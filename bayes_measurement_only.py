#!/usr/bin/env python
import numpy as np

# index 0 means open
# index 1 means closed

# rows are measurements, columns are priors
measurement_model = np.array(
   [ [ 0.9, 0.5 ],
     [ 0.1, 0.5 ] ]
)

bel = np.array(
    [ [ 0.5 ],
      [ 0.5 ] ]
)

measurements = [ 0, 0, 0, 0, 0, 1, 0, 0 ]

for measurement in measurements:
    unnormalized_posterior = (
        measurement_model * \
        np.repeat(bel, 2, axis=1).transpose())[measurement]
    posterior = unnormalized_posterior / sum(unnormalized_posterior)
    print(round(posterior[0], 3))
    bel = np.array([ posterior ]).transpose()
