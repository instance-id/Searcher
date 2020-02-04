# encoding: UTF-8

import re


class Processor(object):
    """An abstract base class that defines the protocol for Processor objects.
    """

    def __init__(self, iterable):
        """Given an iterable of objects, become an iterable of other objects.

        The two sets of objects need not be the same type.

        Note that a file-like object is an iterable of lines.
        """
        self._iterable = iterable
        self.errors = []

    @property
    def iterable(self):
        for thing in self._iterable:
            self.check_input_value(thing)
            yield thing

    def check_input_value(self, value):
        pass

    def has_failed(self, original, result):
        """Given two iterables, representing the input and the output
        of this Processor, return a boolean indicating whether we think
        this Processor has failed or not.
        """
        return False

    def __iter__(self):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__


class LineProcessor(Processor):

    def check_input_value(self, value):
        assert isinstance(value, unicode)


class TrailingWhitespaceProcessor(LineProcessor):

    def __iter__(self):
        for line in self.iterable:
            yield line.rstrip()


class SentinelProcessor(LineProcessor):
    """Yields only those lines of the input between the start
    sentinel (exclusive) and the end sentinel (exclusive.)
    
    The start sentinel is actually "super-exclusive" in that neither it,
    nor any non-blank lines immediately following it, are included in
    the output.

    Note that cleaned lines are stripped of trailing whitespace.
    """

    def __iter__(self):
        self.state = 'pre'
        for line in self.iterable:
            line = line.rstrip()
            if self.state == 'pre':
                match = re.match(self.START_RE, line.upper())
                if match:
                    self.state = 'consuming-start'
            elif self.state == 'consuming-start':
                if not line:
                    self.state = 'mid'
            elif self.state == 'mid':
                match = re.match(self.END_RE, line.upper())
                if match:
                    self.state = 'post'
                else:
                    yield line
            else:
                assert self.state == 'post'
                pass


class ComposedProcessor(LineProcessor):
    """A Processor which applies multiple Processors to an input in
    sequence.  If any Processor fails, it returns the result of
    processing only up to the point of the failure.
    """

    def __init__(self, lines, classes, name=''):
        LineProcessor.__init__(self, lines)
        self.classes = classes
        self.name = name

    def __iter__(self):
        lines = list(self.iterable)
        for cls in self.classes:
            filter_ = cls(lines)
            new_lines = list(filter_)
            if filter_.has_failed(lines, new_lines):
                self.errors.append("%s failed to clean '%s'" % (filter_, self.name))
                break
            lines = new_lines

        for line in lines:
            yield line


class RewritingProcessor(LineProcessor):
    SUBSTITUTIONS = ()

    def rewrite_line(self, subject, replacement, line):
        count = 1
        while count > 0:
            (line, count) = re.subn(subject, replacement, line)
        return line

    def __iter__(self):
        for line in self.iterable:
            line = line.rstrip()
            for (subject, replacement) in self.SUBSTITUTIONS:
                line = self.rewrite_line(subject, replacement, line)
            yield line


class TidyPunctuationLineFilter(RewritingProcessor):
    SUBSTITUTIONS = (
        (ur'- ', u'-'),
        (ur' ,', u','),
        (ur' \.', u'.'),
        (ur' \;', u';'),
        (ur' \:', u':'),
        (ur' \?', u'?'),
        (ur' \!', u'!'),
        (ur',,', u','),
        (ur',\.', u'.'),
        (ur'“ ', u'“'),
        (ur' ”', u'”'),
    )


class FixProductiveEndingsLineFilter(RewritingProcessor):
    SUBSTITUTIONS = (
        (r'olfs ', 'olves '),
        (r'xs', 'xes'),
        (r'ullly', 'ully'),
        (r'yly', 'ily'),
        (r'icly', 'ically'),
        (r'lely', 'ly'),
        (r' coily', ' coyly'),
    )


class FixIndefiniteArticlesLineFilter(RewritingProcessor):
    SUBSTITUTIONS = (
        (r' An unique', ' A unique'),
        (r' an unique', ' a unique'),
        (r' An unicorn', ' A unicorn'),
        (r' an unicorn', ' a unicorn'),
    )


class QuoteOrienterLineFilter(LineProcessor):
    """Note that this expects to work on a single paragraph
    only.  (If you give it more than one paragraph, it will
    happily match quotes between adjacent paragraphs, which
    is probably not what you want.)
    """

    def __iter__(self):
        self.state = 0
        for line in self.iterable:
            new_line = u''
            for character in line:
                character = unicode(character)
                if character == u'"':
                    if self.state == 0:
                        character = u'“'
                        self.state = 1
                    else:
                        assert self.state == 1
                        character = u'”'
                        self.state = 0
                new_line += character
            yield new_line


class Regrouper(Processor):
    """An abstract class that defines the protocol for Regrouper objects."""
    pass


class LinesToParagraphsRegrouper(Regrouper):
    """A Regrouper that groups lines into paragraphs and collections of
    intervening blank lines.
    """

    def __iter__(self):
        state = 'begin'
        group = []
        for line in self.iterable:
            line = line.rstrip()
            if line:
                if state == 'begin':
                    state = 'para'
                    group.append(line)
                elif state == 'para':
                    group.append(line)
                else:
                    assert state == 'blank'
                    yield group
                    state = 'para'
                    group = []
                    group.append(line)
            else:
                if state == 'begin':
                    state = 'blank'
                    group.append(line)
                elif state == 'blank':
                    group.append(line)
                else:
                    assert state == 'para'
                    yield group
                    state = 'blank'
                    group = []
                    group.append(line)
        if group:
            yield group


class ParagraphsToLinesRegrouper(Regrouper):
    """A Regrouper that ungroups paragraphs (and collections of blank lines)
    into individual lines.
    """

    def check_input_value(self, value):
        assert isinstance(value, list)
        for element in value:
            assert isinstance(element, unicode)

    def __iter__(self):
        for para in self.iterable:
            for line in para:
                yield line
