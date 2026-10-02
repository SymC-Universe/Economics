from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np

RIDGE=1e-4
MAX_ITER=100
GRAD_TOL=1e-8
HESSIAN_COND_MAX=1e10

@dataclass(frozen=True)
class EventHistoryFit:
    status:str
    config:str
    rho:float|None
    beta:np.ndarray|None
    iterations:int
    gradient_max_norm:float
    hessian_condition:float
    log_likelihood:float
    reason:str


def causal_excitation(events:np.ndarray,rho:float)->np.ndarray:
    y=np.asarray(events,dtype=float)
    if y.ndim!=1:
        raise ValueError("events must be 1D")
    if not (0.0<rho<1.0):
        raise ValueError("rho must lie in (0,1)")
    out=np.zeros(len(y),dtype=float)
    for t in range(1,len(y)):
        out[t]=rho*out[t-1]+y[t-1]
    return out
def build_event_history_design(
    session_phase:np.ndarray,
    activity_proxy:np.ndarray,
    events:np.ndarray,
    *,
    config:str,
    rho:float|None=None,
    queue_proxy:np.ndarray|None=None,
)->np.ndarray:
    phase=np.asarray(session_phase,dtype=float)
    activity=np.asarray(activity_proxy,dtype=float)
    y=np.asarray(events,dtype=float)
    if phase.ndim!=2 or phase.shape[1]!=4:
        raise ValueError("session_phase must be n x 4")
    n=len(y)
    if len(activity)!=n or len(phase)!=n:
        raise ValueError("length mismatch")
    if np.any(~np.isfinite(phase)) or np.any(~np.isfinite(activity)):
        raise ValueError("nonfinite background covariate")
    cols=[np.ones(n,dtype=float),phase[:,0],phase[:,1],phase[:,2],phase[:,3],activity]
    if config in {"H1","H2"}:
        if rho is None:
            raise ValueError("H1/H2 require frozen rho")
        cols.append(causal_excitation(y,rho))
    if config=="H2":
        if queue_proxy is None:
            raise ValueError("H2 requires queue_proxy")
        q=np.asarray(queue_proxy,dtype=float)
        if len(q)!=n or np.any(~np.isfinite(q)):
            raise ValueError("invalid queue_proxy")
        cols.append(q)
    elif config not in {"H0","H1"}:
        raise ValueError("config must be H0/H1/H2")
    return np.column_stack(cols)
def _loglik(X:np.ndarray,y:np.ndarray,beta:np.ndarray)->float:
    eta=np.clip(X@beta,-40.0,40.0)
    ll=float(np.sum(y*eta-np.logaddexp(0.0,eta)))
    return ll-0.5*RIDGE*float(np.sum(beta[1:]**2))


def fit_event_history_logit(
    X:np.ndarray,
    events:np.ndarray,
    *,
    config:str,
    rho:float|None=None,
)->EventHistoryFit:
    X=np.asarray(X,dtype=float)
    y=np.asarray(events,dtype=float)
    if X.ndim!=2 or len(X)!=len(y) or len(X)==0:
        return EventHistoryFit("REFUSED",config,rho,None,0,math.inf,math.inf,-math.inf,"invalid_input")
    if np.any(~np.isfinite(X)) or np.any(~np.isin(y,[0.0,1.0])):
        return EventHistoryFit("REFUSED",config,rho,None,0,math.inf,math.inf,-math.inf,"nonfinite_or_invalid")
    if np.linalg.matrix_rank(X)<X.shape[1]:
        return EventHistoryFit("REFUSED",config,rho,None,0,math.inf,math.inf,-math.inf,"rank_deficient")
    p=X.shape[1]
    beta=np.zeros(p,dtype=float)
    ll=_loglik(X,y,beta)
    penalty=np.eye(p,dtype=float); penalty[0,0]=0.0
    last_cond=math.inf; last_grad=math.inf
    for it in range(1,MAX_ITER+1):
        eta=np.clip(X@beta,-40.0,40.0)
        prob=1.0/(1.0+np.exp(-eta))
        grad=X.T@(y-prob)-RIDGE*(penalty@beta)
        w=prob*(1.0-prob)
        info=X.T@(X*w[:,None])+RIDGE*penalty
        last_cond=float(np.linalg.cond(info))
        last_grad=float(np.max(np.abs(grad)))
        if not math.isfinite(last_cond) or last_cond>HESSIAN_COND_MAX:
            return EventHistoryFit("REFUSED",config,rho,None,it,last_grad,last_cond,ll,"hessian_condition")
        if last_grad<=GRAD_TOL:
            return EventHistoryFit("COMPLETE",config,rho,beta,it,last_grad,last_cond,ll,"converged")
        try:
            step=np.linalg.solve(info,grad)
        except np.linalg.LinAlgError:
            return EventHistoryFit("REFUSED",config,rho,None,it,last_grad,last_cond,ll,"newton_solve_failed")
        accepted=False; factor=1.0
        for _ in range(40):
            candidate=beta+factor*step
            candidate_ll=_loglik(X,y,candidate)
            if math.isfinite(candidate_ll) and candidate_ll>=ll-1e-12:
                beta=candidate; ll=candidate_ll; accepted=True; break
            factor*=0.5
        if not accepted:
            return EventHistoryFit("REFUSED",config,rho,None,it,last_grad,last_cond,ll,"no_improving_step")
    return EventHistoryFit("REFUSED",config,rho,None,MAX_ITER,last_grad,last_cond,ll,"convergence_not_reached")
def predict_event_probability(X:np.ndarray,fit:EventHistoryFit)->np.ndarray:
    if fit.status!="COMPLETE" or fit.beta is None:
        raise ValueError("fit not qualified")
    eta=np.clip(np.asarray(X,dtype=float)@fit.beta,-40.0,40.0)
    p=1.0/(1.0+np.exp(-eta))
    if np.any(~np.isfinite(p)):
        raise FloatingPointError("nonfinite probability")
    return p


def absolute_relative_event_rate_error(predicted:np.ndarray,observed:np.ndarray)->float:
    p=float(np.mean(np.asarray(predicted,dtype=float)))
    y=float(np.mean(np.asarray(observed,dtype=float)))
    if y<=0:
        return 0.0 if p<=1e-15 else math.inf
    return abs(p-y)/y


def excitation_relative_error(fit:EventHistoryFit,true_alpha:float)->float:
    if fit.status!="COMPLETE" or fit.beta is None or fit.config not in {"H1","H2"}:
        return math.nan
    if true_alpha==0:
        return math.nan
    alpha=float(fit.beta[6])
    return abs(alpha-float(true_alpha))/abs(float(true_alpha))
def normalized_background_rmse(predicted:np.ndarray,truth:np.ndarray)->float:
    p=np.asarray(predicted,dtype=float)
    t=np.asarray(truth,dtype=float)
    if p.shape!=t.shape or np.any(~np.isfinite(p)) or np.any(~np.isfinite(t)):
        raise ValueError("invalid background arrays")
    scale=float(np.mean(np.abs(t)))
    if scale<=1e-15:
        return 0.0 if np.allclose(p,t) else math.inf
    return float(np.sqrt(np.mean((p-t)**2))/scale)


def probability_decile_calibration(predicted:np.ndarray,observed:np.ndarray)->list[dict[str,float|int]]:
    p=np.asarray(predicted,dtype=float)
    y=np.asarray(observed,dtype=float)
    if len(p)!=len(y) or len(p)==0:
        raise ValueError("invalid arrays")
    order=np.argsort(p,kind="stable")
    groups=np.array_split(order,10)
    out=[]
    for i,g in enumerate(groups):
        if len(g)==0:
            continue
        out.append({
            "decile":i+1,
            "n":int(len(g)),
            "predicted_mean":float(np.mean(p[g])),
            "observed_mean":float(np.mean(y[g])),
            "absolute_calibration_error":float(abs(np.mean(p[g])-np.mean(y[g]))),
        })
    return out
