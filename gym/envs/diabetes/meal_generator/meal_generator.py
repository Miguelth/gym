import numpy as np

def meal_generator(eating_time=1, premeal_bolus_time=0, meal_uncertainty_grams=20, no_meals=False, seed=None):
    '''Generates random meals

    Four meals per day

    TODO:
        - Add length of day as input variable
    '''

    # Fixing the random seed
    if seed is not None:
        np.random.seed(seed)

    # ==========================================
    # HACK to manually fix the random seed
    # ==========================================
    # np.random.seed(0)

    # Using the base-meals of Anas El Fathis work and adding +-30 mins to the times randomly
    meal_amounts = np.array([40, 80, 60, 30])  + np.random.uniform(-20, 20, 4)
    meal_times = np.array([8*60, 12*60, 18*60, 22*60]) + np.random.choice(np.linspace(-30, 30, 3, dtype=int), 4)

    # Adding guessed meal amount

    guessed_meal_amount = np.zeros_like(meal_amounts)
    for i in range(len(meal_amounts)):
        guessed_meal_amount[i] = meal_amounts[i] + np.random.uniform(-meal_amounts[i]*.3, meal_amounts[i]*.3)


    # Preallocation 'meal_indicator' indicates time of bolus - default 30 minutes before meal
    meal_indicator = np.zeros(2160)
    meals = np.zeros(2160)

    for i in range(len(meal_times)):

        meals[meal_times[i] : meal_times[i] + eating_time] = meal_amounts[i]/eating_time * 1000 /180
        # meal_indicator[meal_times[i] - premeal_bolus_time:meal_times[i]] = meal_amounts[i] * 1000 / 180

        # Changing to guessed meal amount
        meal_indicator[meal_times[i]-premeal_bolus_time:meal_times[i]-premeal_bolus_time + eating_time] = guessed_meal_amount[i]/eating_time * 1000 / 180

    if no_meals:
        meals = np.zeros(2160)
        meal_indicator = np.zeros(2160)

    meal_bolus_indicator = meal_indicator

    return meals, meal_bolus_indicator
