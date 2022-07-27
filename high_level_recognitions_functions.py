from typing import Tuple

from talon import ctrl

position = ctrl.mouse_pos()
from time import sleep
from typing import Union

from talon import Module, actions

mod = Module()


def has_match_images(template_path: str,
                     threshold: float,
                     other_template_path: str = None,
                     gray_comparison: bool = False) -> bool:
    """todo"""
    try:
        matches = actions.user.move_image_relative(template_path,
                                                   disambiguator=0,
                                                   threshold=threshold,
                                                   should_move_mouse=False,
                                                   gray_comparison=gray_comparison)
        print(f' first try : matches={matches}')
        return matches is not None

    except RuntimeError as e:
        raise_exception_if_not_matching_image_problem(e)
        if not other_template_path:
            return False

        try:

            matches = actions.user.move_image_relative(other_template_path,
                                                       disambiguator=0,
                                                       threshold=threshold,
                                                       should_move_mouse=False)
            print(f'second try : matches={matches}')
            return matches is not None
        except RuntimeError as e:
            raise_exception_if_not_matching_image_problem(e)
            return False


# own user actions
@mod.action_class
class UserActions:

    def click_to_that_image_down_way(template_path: str,
                                     disambiguator: Union[int, str] = 0,
                                     threshold: float = 0.80,
                                     xoffset: float = 0,
                                     yoffset: float = 0, gray_comparison: bool = False,
                                     other_template_path: str = None):
        """todo"""
        current_position: Tuple[int, int] = ctrl.mouse_pos()
        saved_mouse_pos = (actions.mouse_x(), actions.mouse_y())
        print(f'current_position={current_position}')
        # print(f'saved_mouse_pos={saved_mouse_pos}')

        for i in range(2):
            try:
                #     def mouse_helper_move_images_relative(template_path: str,
                #                                           template_path_2: str,
                #                                           print_screen: Path,
                #                                           disambiguator: Union[int, str] = 0,
                #                                           threshold: float = 0.80,
                #                                           xoffset: int = 0,
                #                                           yoffset: int = 0,
                #                                           # TODO gray comparison is not used 
                #                                            any longer for now
                #                                           gray_comparison: bool = False,
                #                                           region: Optional[TalonRect] = None,1
                actions.user.move_image_relative(template_path, disambiguator,
                                                 xoffset=xoffset,
                                                 yoffset=yoffset, region=None,
                                                 gray_comparison=gray_comparison,
                                                 threshold=threshold,
                                                 current_position=current_position,
                                                 should_find_lower_than_position=True)
                actions.sleep(0.5)
                actions.mouse_click(0)
                return
            except RuntimeError as e:
                raise_exception_if_not_matching_image_problem(e)
                actions.user.mouse_scroll_down(1)
                sleep(1)
                current_position = ctrl.mouse_pos()
        raise RuntimeError(f'No match for image={template_path} after 8 tries')


def raise_exception_if_not_matching_image_problem(e: RuntimeError):
    if 'No matches for image' in str(e):
        print('Matching image problem, the flow is not interrupted')
    else:
        raise e
