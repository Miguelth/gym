from gym.envs.diabetes import hovorka_base

class HovorkaGaussianInsulin(hovorka_base.HovorkaBase):

    def _update_parameters(self):
        ''' Update parameters of model,
        this is only used for inherited classes'''

        # meal_times = [0]
        # meal_amounts = [0]

        reward_flag = 'gaussian_with_insulin'

        # Initialization flag: 'random' or 'fixed'
        bg_init_flag = 'random'
        # max_insulin_action = 300

        # return meal_times, meal_amounts, reward_flag, bg_init_flag, max_insulin_action

        return reward_flag, bg_init_flag
