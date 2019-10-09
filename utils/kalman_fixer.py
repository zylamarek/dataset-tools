import numpy as np
from pykalman import KalmanFilter


def fix_meta_sequence_kalman(metas):
    measurements = np.ma.asarray(np.zeros((len(metas), 6)))
    for i, meta in enumerate(metas):
        if meta is not None:
            measurements[i] = meta.flatten()
        else:
            measurements[i] = np.ma.masked

    means = np.mean(measurements, axis=0)
    vars = np.var(measurements, axis=0)
    measurements -= means
    measurements /= vars

    kf = KalmanFilter(n_dim_obs=6, n_dim_state=6,
                      observation_covariance=1e4 * np.eye(6),
                      transition_covariance=1e4 * np.eye(6),
                      em_vars=['initial_state_mean', 'initial_state_covariance'])
    kf = kf.em(measurements)

    smoothed, _ = kf.smooth(measurements)
    smoothed *= vars
    smoothed += means
    metas = [np.reshape(sm, (2, 3)) for sm in smoothed]

    return metas
