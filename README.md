<<<<<<< HEAD
## Closing the Gap: Corporate Boards Add More Women when Interlocked with Diverse Peers
=======
WIP!
# Introduction
Provide an overview of the problem and a literature review. You should address: what gap or question are you addressing? What has been done before?
# Methods
### Model description
Describe how your model works in terms of its: agents, interactions, environment, model schedule/timing
* It’s a good idea to use the PARTE and ODD frameworks as a guide 
* Flow charts & visuals are good! Illustrate the sequence of events in your model using a flow chart. Show how the agents operate, how and when interactions happen, the sequence of events in each time step, etc.
* From your model description, someone should be able to implement a version of your model
>>>>>>> e83d394024ffb45a2257141b10f70b1711585c0f

Suibhne Ó Foighil, 4/27/2022, [GitHub](https://github.com/suibhne-ofoighil/cmplxsys530-final-project) Repo

# Introduction

This project is an extension of my senior thesis which researches the dynamics of gender diversification on corporate boards of directors. My thesis provides evidence that the progress towards gender equity has been uneven and clustered, suggesting the election of women directors is better explained by conformance to descriptive norms among a board&#39;s &#39;interlocked

# 1
&#39; peers, over and above two more popular explanations: the business case for gender-diversity and normative pressure from shareholder activists.

## Problem Statement

I analyzed all elections to the boards of the S&amp;P 1500, from 2010 to 2020. However, I assume a specific measure () captures the behavior of shareholder activists, who coerce un-diverse boards into electing women directors. If I recreate this behavior by modeling election outcomes and simulating interventions by shareholder activists, can I replicate the effect that is found empirically? I.e. does the measure actually capture the behavior I think it does?

To test this assumption, I simulate the elections I originally analyzed and use a probabilistic model to determine the outcomes. The determinants are the social learning effect—which is predominant finding of my thesis, where boards conform to descriptive norms for gender diversity among interlocked peers—as well as the level of shareholder interventions—where boards below a given threshold for gender diversity have some additional probability of diversifying. Then, I regress on the simulated elections using as the independent variable and see how the effect varies in parameter space. In summary, I find the effect estimation for **does not** vary with the parameterized level of shareholder activism, suggesting it is not a good measure for their activity.

_ **Justification of the Problem** _

Boards of directors wield substantial power. They monitor, govern, and control the corporation and in the past, boards consisted almost exclusively of men. Progress toward gender diversity has been steady but slow. In May of 2021, 40 years after the first women were elected to major corporate boards, 30% of the directors on S&amp;P 500 companies were women (Larker &amp; Tayan, 2013).

Considering the business case for gender diversity, mounting evidence suggests that it has positive effects on board performance: in constructive risk-taking (Bernile 2018), merger &amp; acquisition performance (Fonseka, 2017; Ravaonorohanta, 2020), firm innovativeness (Torchia, 2011; Post, 2015), etc. However, even if firms were to ignore the evidence supporting the business case, the ethical motivation for gender diversity is clear: equality of representation.

Much of the recent progress has been attributed to the efforts of institutional investors, who target un-diverse boards through &quot;shareholder activism.&quot; The &quot;Big 3&quot; Asset Managers (Blackrock, State Street, and Vanguard) vote against the reelection of directors for un-diverse boards, and their efforts since 2017 are estimated to have increased the rate of diversification by two and a half fold (Gormely et al, 2021). Separately, state governments have legislated for the cause (Hatcher, 2020); a 2018 California Law (SB 826) mandates a progressive quota for women directors, which is widely considered an effective policy for increasing gender diversity (Groves, 2019; Gertsberg et al., 2021).

The success of these tactics may suggest boards need to be coerced into adding women directors. However, this inference conflicts with traditional theories of corporate governance. Institutional Theory predicts firms will adapt to societal norms to maintain legitimacy, by emulating their &quot;important&quot; peers (DiMaggio, 1983). Further, empirical findings suggest boards cluster around the &#39;descriptive norm&#39; for gender diversity—defined here as the averaged observed behavior among one&#39;s peers (Chang et al., 2019). These results suggest boards learn and adapt to changing norms, and do not need direct instruction or coercion.

Disentangling the impact of these external forces (institutional investors and regulators) from internal forces (conformance to descriptive norms) has important implications for understanding the trend towards gender parity: is this socio-normative effect distinct from the &#39;activism&#39; of institutional investors and policies of regulators? Or is it a result of their actions?

To answer this question, we first must understand the mechanisms that support descriptive norms: how do boards learn the norm and what peers do they observe?

In my thesis, I find evidence that a board&#39;s interlocks create a local descriptive norm for gender diversity which signals when the boards should diversify; Interlocked directors infer what is normal on their connected boards, and bring that experience to the next director election.

# Methods

While I use the empirical interlock network (_network._gexf) and timeseries of elections (_elections.csv_) in my simulations, I determine the outcomes of each election using a probabilistic model, which depends on a board&#39;s relative diversity as compared to its interlocked peers, as well as the interventions of shareholder activists.

## Flow Summary

![](RackMultipart20220428-1-h3uzsg_html_be415284cb0f6704.gif)

| **Parameters** | **Description** | **Value Range** |
| --- | --- | --- |
|

 |
The differential probability of electing a women director, per percentage difference in the board&#39;s gender diversity and the average among its interlocked peers.
 |


 |
|

 |
After 2016, shareholder activists intervene in all elections where the boards are less diverse than the intervention threshold and where the internal decision is to elect a man
 |

 |
|


 |
The probability that the shareholders successfully intervene, and the board elects a woman director
 |


 |

### Initialization

The model&#39;s initialization s very simple: I create deep copies of the empirical networks found in the &quot;init-data&quot; folder. This enables the model to update future instances of the board as a result of the simulated elections, without changing the underlying data—which future generations rely on.

_ **Agents** _
 Boards have the following qualities:

1. _The number of directors_ ()—which does not vary over time. I assume all elections are replacements for outgoing directors to simplify the update function. For a complete justification for this assumption, see Appendix A1.
2. _The number of women directors_ ()—which varies and depends on the outcomes of the simulated elections.
3. _The set of interlocked peers_—who form the local descriptive norm for gender diversity and are connected by unweighted, undirected edges. The network structure is from the inputted networks. There are 10, each corresponding to its respective year [2010, 2020].

### Measure

I define a simple measurement of relative diversity: Deviation from the Descriptive Norm (). To compute , consider an arbitrary board , take its percentage of women directors , and the mean among an arbitrary set of peers : . Then, calculate the difference:

is analogous to statistical deviation and is useful because we can vary the set of peers, thus the descriptive norm, and calculate the board&#39;s relative diversity considering it.

### Elections

When a board is up for an election, I simulate the outcome with 2 probabilistic functions: the _Internal Decision_ and _Shareholder Intervention_. With the _Internal Decision,_ the outcome depends on a base-rate probability for electing a women director (which is , as 30% of the observed elections were of women directors) and a differential probability determined by the board&#39;s relative diversity among its interlocked peers () and the coefficient on this variable (The model parameter: ):

After 2016, for all elections to boards below the intervention threshold (), if the board&#39;s previous _Internal Decision_ did not result in a woman director, the shareholders intervene and attempt to elect a woman director with probability.

### Time

In terms of the order of operations, I loop through all of elections in _elections._csv and simulate their outcomes. If a woman is successfully elected—irrespective if it is a result of an _internal decision_ or a _shareholder intervention_—the number of women directors is incremented, for each instance of the board in the successive networks. For example, if a board elects a woman director in 2012 and appears again in the 2015, 2018, and 2020 networks, because of the 2012 election, the number of women on those latter instances will be of 1 more than that of 2012.

### Environment

I will use a network-based model where the nodes are boards, and the edges are interlocked directors. It is an unweighted, undirected network, that varies from year to year: 2010-2020.

## Model analysis

In my thesis, I find is a significant determinant for the election of women directors in 2017-2020, but not 2010-2016 (see Appendix A2). This shows a change in board behavior coinciding with increased shareholder activism, as institutional investors intervene in boards elections from 2017 onwards. Thus, the goal is to understand how the effect estimation on varies with the model parameters.

To do this, I simulate 1000 generations and fit a GEE regression to each. Then, I compare the regressed effects with the corresponding parameters. I sample parameter space using Latin Hypercube Sampling. For each election, I record the gender of the elected director; the board&#39;s relative diversity among interlocked peers (); and the board&#39;s relative diversity compared to the network ().

# Results

The simulations produce surprising results: varies tightly with —which was also clear from my thesis analysis. However, while has loose correlation with the , there seems to be no relationship between and the . Moreover, _Shareholder Interventions_—which only occur in 2017-2020—seem to have an immaterial effect on the effect estimation of , suggesting **it is not** a good measure for shareholder activism:

![](RackMultipart20220428-1-h3uzsg_html_a9db7b80bffcdea1.png) ![](RackMultipart20220428-1-h3uzsg_html_ae08095542c97b28.png) ![](RackMultipart20220428-1-h3uzsg_html_d43fa26c13e5622c.png) ![](RackMultipart20220428-1-h3uzsg_html_e06d9e4d94d48f42.png) ![](RackMultipart20220428-1-h3uzsg_html_815daddb71b45e03.png) ![](RackMultipart20220428-1-h3uzsg_html_587f91615549c619.png)

![](RackMultipart20220428-1-h3uzsg_html_cdcd166f149e7371.png) ![](RackMultipart20220428-1-h3uzsg_html_785bcc3eb945e359.png) ![](RackMultipart20220428-1-h3uzsg_html_4209162903b36c4b.png) ![](RackMultipart20220428-1-h3uzsg_html_574bc02358b7a5b4.png) ![](RackMultipart20220428-1-h3uzsg_html_e07a9d55fe654189.png) ![](RackMultipart20220428-1-h3uzsg_html_8e29031ace8da7b7.png)

![](RackMultipart20220428-1-h3uzsg_html_9ad7519a684bfb64.png)

However, relative to the empirical estimation (the red, vertical line), the distribution of regressed coefficient for is off for both periods. Because of this, I don&#39;t think can conclude is a bad measure, as there may be relevant factors to the estimation of , which we don&#39;t account for.

![](RackMultipart20220428-1-h3uzsg_html_bc352f3e25a96607.png) ![](RackMultipart20220428-1-h3uzsg_html_5cdc8e6bd6976010.png)

# Discussion

With this model, we saw the GEE estimation for the effect of did not vary with the assumed level of shareholder activism—the andmodel parameters—suggesting is not a good measure of shareholder activism. However, there are significant limitations to this inference, considering the assumptions I made on the behavior of the boards. For instance, I only use a board&#39;s relative diversity among interlocked peers to differentiate its probability of electing a women director, and I assume that intrinsic preferences for gender diversity are homogenous among all boards by using a base-rate probability (30%). From my thesis, I know the probability of electing a woman director varies by sector and that boards preferentially attach to their sector peers. So, this assumption of homogeneity is potentially problematic. Extensions of the model will use more empirical data to differentiate the election probabilities of boards, which would better substantiate inferences on more solid ground.

## **References**

Bernile, G., Bhagwat, V., &amp; Yonker, S. (2018). Board diversity, firm risk, and corporate policies. Journal of financial economics, 127(3), 588-612.

Byron, K., &amp; Post, C. (2016). Women on boards of directors and corporate social performance: A meta‐analysis. Corporate Governance: An International Review, 24(4), 428-442.

Chang, E. H., Milkman, K. L., Chugh, D., &amp; Akinola, M. (2019). Diversity thresholds: How social norms, visibility, and scrutiny relate to group composition. Academy of Management Journal, 62(1), 144-171.

DiMaggio, P. J., &amp; Powell, W. W. (1983). The iron cage revisited: Institutional isomorphism and collective rationality in organizational fields. American sociological review, 147-160.

Fonseka, M. M., &amp; Tian, G. L. (2017). Gender Diversity in the Boardroom on Private Equity Placements: Evidence from China. Available at SSRN 2565257.

Gertsberg, M., Mollerstrom, J., &amp; Pagel, M. (2021). _Gender quotas and support for women in board elections_ (No. w28463). National Bureau of Economic Research.

Gormley, T. A., Gupta, V. K., Matsa, D. A., Mortal, S., &amp; Yang, L. (2021). The big three and board gender diversity: The effectiveness of shareholder voice. European Corporate Governance Institute–Finance Working Paper, 714, 2020.

Groves, M. (2019, December 17). How California&#39;s &#39;woman quota&#39; is already changing corporate boards. CalMatters. Retrieved March 24, 2022, from [https://calmatters.org/economy/2019/12/california-woman-quota-corporate-board-gender-diversity/](https://calmatters.org/economy/2019/12/california-woman-quota-corporate-board-gender-diversity/)

Hatcher, M., Latham, W., &amp; Lewis, J. (2020). States are leading the charge to corporate boards: Diversify! Harvard Law School Forum on Corporate Governance.

Larcker, D. F., &amp; Tayan, B. (2013). Pioneering women on boards: Pathways of the first female directors. Rock Center for Corporate Governance at Stanford University Closer Look Series: Topics, Issues and Controversies in Corporate Governance and Leadership No. CGRP-35.

Post, C., &amp; Byron, K. (2015). Women on boards and firm financial performance: A meta-analysis. Academy of management Journal, 58(5), 1546-1571.

Ravaonorohanta, N. (2020). GENDER-DIVERSE BOARDS GET BETTER PERFORMANCE ON MERGERS AND ACQUISITIONS.

Torchia, M., Calabrò, A., &amp; Huse, M. (2011). Women Directors on Corporate Boards: From Tokenism to Critical Mass. Journal of Business Ethics, 102(2), 299–317. http://www.jstor.org/stable/41475957

## **Appendix**

### A1: Justification for the Elections as Replacements Assumption

In terms of how and when directors are nominated, many of the elections in the observed sample are effectively replacements for out-going directors, because I exclude founding board members and are probably not a result of board expansions, as average board size has remained constant:

![](RackMultipart20220428-1-h3uzsg_html_ed979b3160c4335.png)

Considering the rate of additions to boards, companies elect directors at a steady cadence—about once per year—with little variability in averaged rates: Median elections / year ≈ 0.86, Mean ≈ 0.93, Standard Deviation ≈ 0.49. Specifically, &quot;averaged&quot; rates are computed for each firm by summing the number of elections during the full period (2010-2020), and by dividing the sum by the number of years in the active period: the year of the first election to 2020, inclusive of both.

Looking at the time-distribution of additions, I find significant bias is my sample. The number of elections in 2020 is roughly double that of 2010—667 to 1272. Further, the number of boards adding directors in 2020 is about double that of 2010—478 to 805. This can be attributed to two things: 1) the sample selection—this is the 2021 S&amp;P 1500 and the number of firms may increase over time; and 2), it could be that the behavior of the boards changed over time:

![](RackMultipart20220428-1-h3uzsg_html_205272faf9ef5341.png) ![](RackMultipart20220428-1-h3uzsg_html_a38f19cdf9b7e74d.png) ![](RackMultipart20220428-1-h3uzsg_html_e8fe490b230d7557.png)

In the interlock network, we include companies in each year if they are listed on the public markets. We see the number of S&amp;P 1500 boards remained constant from 2010 to 2020 (around 1150 boards in each year). This suggests the time bias is more a factor of changing behavior; not a result of the number of firms increasing over time:

| Year | _Nodes_ | _Proportion of Nodes in S&amp;P 1500_ | _Edges_ | _Average Degree_ | _Percentage of Nodes in Giant Component_ | _Percentage Women Correlation_ |
| --- | --- | --- | --- | --- | --- | --- |
| 2010 | 2745 | 42% | 6432 | 7.69 | 94% | 22% |
| 2011 | 2730 | 42% | 6620 | 7.83 | 94% | 22% |
| 2012 | 2752 | 42% | 6807 | 7.96 | 95% | 21% |
| 2013 | 2855 | 40% | 7114 | 8.08 | 95% | 21% |
| 2014 | 2949 | 39% | 7360 | 8.17 | 95% | 20% |
| 2015 | 3067 | 37% | 7788 | 8.52 | 96% | 20% |
| 2016 | 2953 | 39% | 7640 | 8.41 | 96% | 20% |
| 2017 | 2912 | 39% | 7574 | 8.32 | 96% | 20% |
| 2018 | 2903 | 40% | 7636 | 8.40 | 96% | 19% |
| 2019 | 2901 | 40% | 7818 | 8.62 | 97% | 18% |
| 2020 | 2965 | 39% | 7966 | 8.67 | 97% | 14% |

### A2: Empirical Estimations of globalDEV

![](RackMultipart20220428-1-h3uzsg_html_f7246e575b20ccef.png)

[1](#sdfootnote1anc) Because directors are not day-to-day managers of the firm, and typically meet 4 times a year to make long-term decisions, they often work at multiple firms simultaneously. If a director works at both firms, they are &#39;interlocked&#39;