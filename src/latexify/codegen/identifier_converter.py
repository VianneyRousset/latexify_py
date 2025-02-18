"""Utility to convert identifiers."""

from __future__ import annotations

from latexify.codegen import expression_rules


class IdentifierConverter:
    r"""Converts Python identifiers to appropriate LaTeX expression.

    This converter applies following rules:
        - `foo` --> `\foo`, if `use_math_symbols == True` and the given identifier
          matches a supported math symbol name.
        - `x` --> `x`, if the given identifier is exactly 1 character (except `_`)
        - `foo_bar` --> `\mathrm{foo\_bar}`, otherwise.
    """

    _use_math_symbols: bool
    _use_mathrm: bool

    def __init__(self, *, use_math_symbols: bool, use_mathrm: bool = True) -> None:
        r"""Initializer.

        Args:
            use_math_symbols: Whether to convert identifiers with math symbol names to
                appropriate LaTeX command.
            use_mathrm: Whether to wrap the resulting expression by \mathrm, if
                applicable.
        """
        self._use_math_symbols = use_math_symbols
        self._use_mathrm = use_mathrm

    def convert(self, name: str) -> tuple[str, bool]:
        """Converts Python identifier to LaTeX expression.

        Args:
            name: Identifier name.

        Returns:
            Tuple of following values:
                - latex: Corresponding LaTeX expression.
                - is_single_character: Whether `latex` can be treated as a single
                    character or not.
        """

        parts = name.split("_")

        if len(parts) > 1:
            other = "_".join(parts[1:])
            other = self.convert(other)[0]
            return self.convert(parts[0])[0] + "_{" + other + "}", False

        if self._use_math_symbols:

            try:
                return "\\" + expression_rules.MATH_SYMBOLS[name], True

            except KeyError:
                pass

        if len(name) == 1 and name != "_":
            return name, True

        wrapped = rf"\mathrm{{{name}}}" if self._use_mathrm else name

        return wrapped, False
