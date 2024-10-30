from math import ceil


class CustomPaginator:
    def __init__(self, page, size, total):
        """
        Initialize the Paginator.

        :param page: The current page number (1-based).
        :param size: The number of items per page.
        :param total: The total number of items.
        """
        self.page_size = size
        self.current_page = page
        self.items = total
        self.pages = ceil(total / size)
        self.next_page = page + 1 if page < self.pages else None
        self.previous_page = page - 1 if page > 1 else None

    def pages_range(self, *, on_each_side=2, on_ends=2):
        """
        Generate a list of page numbers to display, including ellipses to shorten
        the range if the total number of pages is large.

        :param on_each_side: The number of pages to display on each side of the current page.
        :param on_ends: The number of pages to display at the beginning and end of the pagination range.
        :return: A list of page numbers and ellipses ('...') indicating skipped ranges.

        Example:
        If there are 20 pages and the current page is 10, with on_each_side=2 and on_ends=2, 
        the output would be:
        [1, 2, '...', 8, 9, 10, 11, 12, '...', 19, 20]
        """
        max_display = on_each_side * 2 + on_ends * 2 + 1

        # If the total number of pages is less than or equal to max_display, show all pages.
        if self.pages <= max_display:
            return list(range(1, self.pages + 1))

        # Calculate the start and end of the middle range around the current page.
        start = max(1, self.current_page - on_each_side)
        end = min(self.pages, self.current_page + on_each_side)

        middle = list(range(start, end + 1))

        # Determine the beginning of the range (with potential ellipsis).
        if start > on_ends + 1:
            beginning = list(range(1, on_ends + 1)) + ['...']
        else:
            beginning = list(range(1, start))

        # Determine the ending of the range (with potential ellipsis).
        if end < self.pages - on_ends:
            ending = ['...'] + \
                list(range(self.pages - on_ends + 1, self.pages + 1))
        else:
            ending = list(range(end + 1, self.pages + 1))

        # Combine the beginning, middle, and ending ranges.
        return beginning + middle + ending

    def __repr__(self):
        """
        Provide a string representation of the Paginator object.

        :return: A string representation of the paginator, showing its key properties.
        """
        return (f"Paginator(page_size={self.page_size}, current_page={self.current_page}, "
                f"items={self.items}, pages={self.pages}, "
                f"next_page={self.next_page}, previous_page={self.previous_page})")
