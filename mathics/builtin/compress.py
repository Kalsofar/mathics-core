# -*- coding: utf-8 -*-


import base64
import zlib

from mathics.builtin.base import Builtin
from mathics.core.atoms import String


class Compress(Builtin):
    """
    <dl>
    <dt>'Compress[$expr$]'
      <dd>gives a compressed string representation of $expr$.
    </dl>

    >> Compress[N[Pi, 10]]
     = eJwz1jM0MTS1NDIzNQEADRsCNw==

    """

    attributes = ("Protected",)

    options = {
        "Method": "{}",
    }

    def apply(self, expr, evaluation, options):
        "Compress[expr_, OptionsPattern[Compress]]"
        if isinstance(expr, String):
            string = '"' + expr.value + '"'
        else:
            string = expr.format(evaluation, "System`FullForm")
            string = string.boxes_to_text(
                evaluation=evaluation, show_string_characters=True
            )
        string = string.encode("utf-8")

        # TODO Implement other Methods
        # Shouldn't be this a ByteArray?
        result = zlib.compress(string)
        result = base64.b64encode(result).decode("utf8")
        return String(result)


class Uncompress(Builtin):
    """
    <dl>
    <dt>'Uncompress["$string$"]'
      <dd>recovers an expression from a string generated by 'Compress'.
    </dl>

    >> Compress["Mathics is cool"]
     = eJxT8k0sychMLlbILFZIzs/PUQIANFwF1w==
    >> Uncompress[%]
     = Mathics is cool

    >> a = x ^ 2 + y Sin[x] + 10 Log[15];
    >> b = Compress[a];
    >> Uncompress[b]
     = x ^ 2 + y Sin[x] + 10 Log[15]
    """

    attributes = ("Protected",)

    def apply(self, string, evaluation):
        "Uncompress[string_String]"
        string = string.get_string_value()  # .encode("utf-8")
        string = base64.b64decode(string)
        tmp = zlib.decompress(string)
        tmp = tmp.decode("utf-8")
        return evaluation.parse(tmp)
