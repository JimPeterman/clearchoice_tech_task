# Answers to Case Study Questions

## A basic summary of my work:

### *A list of the features that your model uses. Include descriptions for the features you engineered, if any.*
The provided features include in the model are: 
- "lead_segment_20_c"
- "has_email"
- "in_market"
- "created_by_channel"
- "sched_source"
- "apts_in_next_seven_c"
- "apt_hr
- "num_campaigns"

I also include these engineered features in the final model:
- "dental_condition_consolidated": a consolidated list of dental conditions that were entered. 
- "apt_date_day": The day of the week (eg, Monday) of the scheduled appointment.
- "distance_to_center_conslidated": Made distances greater than 250 miles just 250 miles.
- "days_created_to_scheduling": The number of days from when the patient was first created in the system to when they scheduled their appointment. 
- "days_created_to_appointment": The number of days from the date when the patient was first created in the system to the date of their appointment. 
- "days_scheduling_to_appointment": The number of days between when the patient scheduled their appointment and when the appointment was scheduled for. 

### *The relevant performance metrics that you used in model evaluation. Include metric name and values for your model.*
When assessing the models, I calculated measures of accuracy, recall, precision, and F1. However, with the imbalanced distribution of the target (~25% of the dataset included those who actually showed up to their appointment), accuracy is not the ideal metric. The *primary* metric I used was precision because I am thinking it's more important to get bodies in the door so it's ok to overbook (in other words, the greater concern is false positives rather than false negatives).
The precision value for my final model tested on holdout data was: 67.8%. 

## Your concise answers to the following questions:
### *What features, if any, did you decide to exclude from the original dataset? How did you decide?*
- I excluded "start" and "revenue_sold" from the analysis. I excluded these primarily because they are determined after someone shows up to an appointment, so they would not be available when trying to predict if a new customer will show up to their first appointment. 
- I did not include "lead_number" as this was an arbitrary number. 
- I did not include the original "dental_condition" because there was such a spread of entries and some overlap. 
- I did not include dates as these features would be associated with a lot of potential confounders and therefore limited in their usefulness in the future.
- I did not include "PrevNoShows" since this would not be helpful for first time customers (and was automatically filled with a 0 rather than NA it seems). 
- I excluded "first_campaign_type" and "last_campaign_type" for this initial analysis because of the wide range of potential responses - I'd want a better understanding of how these responses could be consolidated/combined.
- For the final model, I ultimately did not include the 3rd party features ("estimated_income_max_c", "estimated_income_min_c", "economic_stability_indicator_c", "atp_value", "affluence_index_value", "vantage_score_neighborhood_risk_score_value", "total_liquid_investible_assets_c", or "income_360_value") as these did not add to the precision of the model.

### *What are the strengths and weaknesses of your model in classifying whether a patient will arrive at their appointment or not?*
-Strengths: The model improves scheduling capabilities by providing the ability to predict whether a customer will show up. Additionally, the model identifies the top predictors for whether a customer will show up, which indicates opportunities to improve outreach and get customers through the door. 

-Weaknesses: The final model predicts less people will show up than what will actually happen. This could be problematic for staff at the clinics in which case a different model performance metric should be used. Additionally, it appears the dataset includes first time and repeat customers. I suspect a seperate model for these two groups would be beneficial and improve performance. Identifying other features could also potentially improve performance. 

### *Broadly speaking, what steps do you think would be necessary to implement this model in production?*
1. Confirm the data collection/availability from potential customers, to ensure the model will have the necessary inputs.
2. Finalize model and feature selection.
3. Containerize the model.
4. Work with backend developers to include needed feature engineering (eg, determining days between scheduling and appointment).
5. Develop monitoring alerts/error handling: input values outside of expected ranges, worsening model performance
6. Deploy model. 
