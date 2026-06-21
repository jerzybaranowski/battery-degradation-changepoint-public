# Figure manifest

All figures use the publication profile, 300-DPI PNG export, embedded PDF fonts,
and frozen accepted analytical artifacts. Generated filenames match the
manuscript filenames.

## Figure 1 — `fig_results_cd_trajectories`

- Module: `battery_degradation_publication.figures.cd_trajectories`
- Accepted runs: `m5_h5_1_full_metric_final`, `m4_bayesian_smooth`
- Inputs: frozen regular-eligible per-battery rows and complete cycle aggregate
- Raw data required: no
- Caveat: the aggregate support filter is not raw-row deletion.

Battery-level and aggregate evolution of the charging-to-discharge duration
ratio. Panel (a) shows the regular-eligible trajectories for the 14 reconstructed
battery records. Panel (b) shows the cycle-level median and interquartile range;
open markers identify cycles with fewer than seven contributing batteries.
Panel (c) shows aggregate support and the seven-battery threshold used for the
model-facing dataset.

## Figure 2 — `fig_results_transition_definitions`

- Module: `battery_degradation_publication.figures.transition_definitions`
- Accepted run: `m4_changepoint_definitions`
- Inputs: frozen method summaries, fitted trajectories, and curvature sensitivity
- Caveat: breakpoint, smooth midpoint, and curvature knee are non-equivalent estimands.

Comparison of operational transition definitions on the aggregate trajectory.
Panel (a) shows the no-changepoint linear reference, continuous broken-stick
fit, and Bayesian smooth-hinge latent trajectory. Shaded vertical intervals
denote the broken-stick moving-block-bootstrap interval and aggregate Bayesian
95% highest-density interval. Panel (b) shows that the smoothing-spline
curvature knee varies substantially with smoothing and fails its stability gate.
These locations are related but non-equivalent estimands.

## Figure 3 — `fig_results_h5_transition_midpoints`

- Module: `battery_degradation_publication.figures.h5_transition_midpoints`
- Accepted run: `m5_h5_1_full_metric_final`
- Inputs: frozen battery and population posterior summaries
- Caveat: Battery 11 is boundary-sensitive but retained.

Battery-specific smooth-transition midpoints from the accepted hierarchical
model. Points denote posterior medians and horizontal intervals denote 95%
highest-density intervals. The population marker is the posterior distribution
of the draw-wise mean of the battery-specific midpoints. Transition timing
varies substantially across batteries; Battery 14 is earliest, whereas Battery
11 is latest and boundary-sensitive but retained.

## Figure 4 — `fig_results_h5_slope_acceleration`

- Module: `battery_degradation_publication.figures.h5_slope_acceleration`
- Accepted run: `m5_h5_1_full_metric_final`
- Inputs: frozen battery and population slope summaries
- Caveat: degradation direction is indicator-dependent; positive is accelerated for `C/D`.

Battery-specific degradation-rate slopes and slope increments under the accepted
hierarchical model. Panel (a) compares posterior-median pre- and post-transition
slopes. Panel (b) shows posterior medians and 95% highest-density intervals for
slope increments, with zero as a reference. Population draw-wise summaries are
shown separately. All 14 batteries have posterior probability one of a positive
slope increment.

## Figure 5 — `fig_results_h5_selected_fits`

- Module: `battery_degradation_publication.figures.h5_selected_fits`
- Accepted run: `m5_h5_1_full_metric_final`
- Inputs: frozen trajectory and transition summaries
- Caveat: bands are latent-mean intervals, not posterior predictive intervals.

Representative battery-level fits from the accepted hierarchical model. The
panels show Battery 14 as an early transition, Battery 1 near the population
midpoint, Battery 3 as a later well-identified transition, and boundary-sensitive
Battery 11. Curves are posterior median latent trajectories with 90% latent-mean
intervals; vertical lines and shaded regions denote battery-specific transition
midpoint medians and 95% highest-density intervals.

## Figure 6 — `fig_results_h5_ppc`

- Module: `battery_degradation_publication.figures.h5_ppc`
- Accepted run: `m5_h5_1_full_metric_final`
- Inputs: frozen overall, battery, and binned residual PPC summaries
- Caveat: predictive miscalibration does not imply failed MCMC convergence.

Posterior predictive assessment of the hierarchical model. Panel (a) compares
nominal and empirical central predictive coverage. Panels (b) and (c) show
within-battery binned residual summaries over normalized cycle position. Panel
(d) shows battery-specific 90% and 95% coverage; Battery 11 uses
boundary-sensitive styling. Coverage is below nominal at 90% and 95%, signed
residual bias is small, and residual magnitude increases over the trajectories.
These discrepancies concern observation-model completeness rather than Markov
chain Monte Carlo convergence.

## Figure 7 — `fig_results_random_thinning`

- Module: `battery_degradation_publication.figures.random_thinning`
- Accepted run: `m8_extended_sensitivity_01`
- Inputs: frozen A1/H5.1 stability and diagnostic tables
- Caveat: open aggregate markers are diagnostic-only fits.

Robustness to endpoint-preserving random removal of approximately half the
observations. Panels show population midpoint shifts, 95%
highest-density-interval width ratios, hierarchical battery-rank correlation,
and battery-specific midpoint shifts. Filled markers passed the production
diagnostic gate; open aggregate-model markers are diagnostic-only fits that
failed an effective-sample-size criterion. Random thinning increases transition
uncertainty but largely preserves hierarchical battery ordering and positive
slope acceleration.

## Figure 8 — `fig_results_truncation_sensitivity`

- Module: `battery_degradation_publication.figures.truncation_sensitivity`
- Accepted run: `m8_extended_sensitivity_01`
- Inputs: frozen truncation and computational-diagnostic summaries
- Caveat: A1 and H5.1 use different observation units.

Sensitivity to shortened observation horizons. Panel (a) shows the population
transition-midpoint shift relative to the full-data fit for the aggregate and
hierarchical models. Panel (b) shows the Spearman rank correlation between the
hierarchical battery-specific transition ordering under truncation and the
corresponding full-data ordering. Panel (c) reports extrapolation root-mean-square
error for observations withheld beyond the retained trajectory. Panel (d)
reports empirical coverage of the nominal 90% and 95% posterior predictive
intervals. Filled markers denote fits that passed the production diagnostic
gate, whereas open markers denote diagnostic-only fits. The aggregate-model
result at 70% retention is additionally marked because it contained one
tree-depth saturation.

## Figure 9 — `fig_results_post_transition_horizon`

- Module: `battery_degradation_publication.figures.post_transition_horizon`
- Accepted run: `m8_extended_sensitivity_01`
- Inputs: frozen horizon and identifiability table
- Caveat: displayed associations are descriptive, not causal.

Relationship between available post-transition history and transition
identifiability. Panel (a) relates post-transition horizon to absolute
battery-specific midpoint shift; panel (b) relates the horizon to the 95%
highest-density-interval width ratio. Marker shape encodes the predefined
availability class. Spearman correlations are annotated in each panel. Battery
11 truncation points are labelled and illustrate the most severe
boundary-sensitive behaviour.

## Figure 10 — `fig_results_battery11_truncation`

- Module: `battery_degradation_publication.figures.battery11_truncation`
- Accepted runs: `m5_h5_1_full_metric_final`, `m8_extended_sensitivity_01`
- Inputs: frozen Battery 11 trajectory, truncation summaries, and mask endpoints
- Caveat: partial pooling cannot identify an unobserved individual late regime.

Battery 11 as a transition-localization limit case. The first panel shows the
full trajectory and accepted full-data latent fit; subsequent panels show
retained and withheld observations at each truncation fraction, the full-data
midpoint, and the scenario-specific midpoint. At 90% retention the endpoint lies
only about 67 cycles after the full-data midpoint, short relative to the
approximately 184-cycle common transition width. More severe truncation removes
the individual late regime. Partial pooling preserves positive slope
acceleration but cannot recover an unobserved battery-specific transition
location.
