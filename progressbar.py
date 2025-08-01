'''
Python Wrapper for https://github.com/guibranco/progressbar | made by https://github.com/EchterTimo
'''


from dataclasses import dataclass
from enum import Enum
from requests import Request


class ProgressBarStyle(Enum):
    DEFAULT = 'default'
    FLAT = 'flat'
    SQUARE = 'square'
    PLASTIC = 'plastic'
    FOR_THE_BADGE = 'for-the-badge'
    THIN_ROUNDED = 'thin-rounded'
    NEO_GLASS = 'neo-glass'
    MINIMAL_MATTE = 'minimal-matte'

    def __str__(self):
        return self.value


@dataclass
class ProgressBar:
    value: int = 50
    '''
    The current value of the progress bar.
    Should be in range from 0 to scale.
    Default: 50
    '''
    title: str = None
    '''
    Adds a title to the progress bar.
    Default: None
    '''
    scale: int = 100
    '''
    The maximum value that the progress bar represents.
    Default: 100
    '''
    prefix: str = None
    '''
    A string to add before the progress number.
    Default: None
    '''
    suffix: str = '%'
    '''
    A string to add after the progress number.
    Default: '%'
    '''
    width: int = 100
    '''
    The width of the progress bar in pixels.
    Default: 100
    '''
    color: str = '00ff00'
    '''
    The color of the progress bar (hex code without #).
    Default: '00ff00' (green)
    '''
    progress_background: str = 'ffffff'
    '''
    The background color of the progress bar (hex code without #).
    Default: 'ffffff' (white)
    '''
    progress_number_color: str = '000000'
    '''
    The color of the progress number (hex code without #).
    Default: '000000' (black)
    '''
    progress_color: str = None
    '''
    The color of the progress bar (hex code without #).
    Default: Depends on percentage
    '''
    show_text: bool = True
    '''
    Whether to display or hide the progress text.
    Default: True
    '''
    _title_auto_fill_length: int = 0
    '''
    The length of the title. Missing characters will be filled with spaces.
    Default: 0
    '''

    style: ProgressBarStyle = ProgressBarStyle.DEFAULT

    def get_modified_keys(self):
        '''
        returns a list of keys that have been changed from the default values
        '''
        if self.title is not None and self._title_auto_fill_length > 0:
            self._fill_spaces_title(self._title_auto_fill_length)

        modified_keys: dict = {}
        for key, value in DEFAULT_PROGRESS_BAR.__dict__.items():
            if getattr(self, key) != value:
                if key.startswith('_'):
                    continue
                modified_keys[key] = getattr(self, key)
        return modified_keys

    def _fill_spaces_title(self, target_length: int = 0) -> str:
        """
        Fills the title with spaces to fit the total character count.
        """
        if target_length > 0:
            spaces_to_add = target_length - len(self.title)
            self.title = self.title + ' ' * spaces_to_add
            return self.title
        return self.title

    def generate_url(self):
        """
        Generates the URL for the progress bar using only the parameters
        that differ from the default values.
        """

        url = BASE_URL.format(self.value)
        params = self.get_modified_keys()

        r = Request(
            method='GET',
            url=url,
            params=params
        )
        return r.prepare().url


DEFAULT_PROGRESS_BAR = ProgressBar()
'''
Default progress bar with standard settings.
'''

BASE_URL = 'https://progress-bar.xyz/{}/'

if __name__ == '__main__':
    # example usage
    pb = ProgressBar(
        title='Test Progress',
        width=200,
        style=ProgressBarStyle.FOR_THE_BADGE,
        show_text=False
    )
    print(pb.generate_url())
