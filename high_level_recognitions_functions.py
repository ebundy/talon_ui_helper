from talon import ctrl

position = ctrl.mouse_pos()
from time import sleep
from typing import Union

from talon import Module, actions

mod = Module()


# own user actions
@mod.action_class
class UserActions:

    def has_match_images(template_path: str,
                         threshold: float,
                         other_template_path: str = None,
                         gray_comparison: bool = False,
                         should_find_lower_than_position: bool = False,
                         ) -> bool:
        """todo"""
        try:
            matches = actions.user.move_image_relative(template_path,
                                                       disambiguator=0,
                                                       threshold=threshold,
                                                       should_move_mouse=False,
                                                       gray_comparison=gray_comparison,
                                                       should_find_lower_than_position=should_find_lower_than_position,
                                                       should_notify_message_if_fail=True)
            print(f'has_match_images(): first try : matches={matches}')
            return matches is not None

        except RuntimeError as e:
            raise_exception_if_not_matching_image_problem(e)
            if not other_template_path:
                return False

            try:

                matches = actions.user.move_image_relative(other_template_path,
                                                           disambiguator=0,
                                                           threshold=threshold,
                                                           should_move_mouse=False,
                                                           should_notify_message_if_fail=True,
                                                           should_find_lower_than_position=should_find_lower_than_position,
                                                           )
                print(f'has_match_images(): second try : matches={matches}')
                return matches is not None
            except RuntimeError as e:
                raise_exception_if_not_matching_image_problem(e)
                return False

    def click_to_that_image_down_way(template_path: str,
                                     disambiguator: Union[int, str] = 0,
                                     threshold: float = 0.80,
                                     xoffset: float = 0,
                                     yoffset: float = 0,
                                     gray_comparison: bool = False,
                                     scroll_down_amount: float = 1,
                                     other_template_path: str = None,
                                     max_x_position: float = None):
        """todo"""
        # print(f'current_position={current_position}')

        should_find_lower_than_position = True
        for i in range(3):
            # try:
            print(f'click_to_that_image_down_way() try {i + 1}')
            is_move: bool = actions.user.move_image_relative(template_path,
                                                             disambiguator,
                                                             xoffset=xoffset,
                                                             yoffset=yoffset,
                                                             region=None,
                                                             gray_comparison=gray_comparison,
                                                             should_notify_message_if_fail=False,
                                                             threshold=threshold,
                                                             should_find_lower_than_position=should_find_lower_than_position,
                                                             max_x_position=max_x_position)

            if is_move:
                actions.sleep(0.5)
                actions.mouse_click(0)
                return
            else:
                # raise_exception_if_not_matching_image_problem(e)
                actions.user.mouse_scroll_down(scroll_down_amount)
                sleep(1)
                should_find_lower_than_position = False
        # except RuntimeError as e:
        # raise_exception_if_not_matching_image_problem(e)

        #     actions.user.mouse_scroll_down(scroll_down_amount)
        #     sleep(1)
        #     should_find_lower_than_position = False
        raise RuntimeError(f'No match for image={template_path} after {i + 1} tries')


def raise_exception_if_not_matching_image_problem(e: RuntimeError):
    if 'No matches for image' in str(e):
        print('Matching image problem, the flow is not interrupted')
    else:
        raise e
