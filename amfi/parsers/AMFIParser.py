import re
import requests
from datetime import date, datetime
from typing import Iterator


class AMFIParser:

    FROM_DATE_PARAM = "frmdt"
    TO_DATE_PARAM = "todt"

    def __init__(
        self,
        url: str,
        from_date: date,
        to_date: date = None,
    ) -> None:
        self.url = url
        self.from_date = from_date
        self.to_date = to_date

    def get_data(self):
        params = {
            self.FROM_DATE_PARAM: self.from_date.strftime("%Y-%m-%d"),
            self.TO_DATE_PARAM: None if not self.to_date else self.to_date.strftime("%Y-%m-%d"),
        }
        response = requests.get(self.url, params=params)
        response.raise_for_status()
        return response.text

    def convert_dtypes(self, values):
        int_columns_idx = [0]
        float_columns_idx = [4, 5, 6]
        date_columns_idx = [7]

        for idx in int_columns_idx:
            try:
                values[idx] = int(values[idx])
            except:
                values[idx] = None

        for idx in float_columns_idx:
            try:
                values[idx] = float(values[idx])
            except:
                values[idx] = None

        for idx in date_columns_idx:
            try:
                values[idx] = datetime.strptime(values[idx], "%d-%b-%Y").date()
            except:
                values[idx] = None

    def parse(self) -> Iterator[dict]:
        data = self.get_data()
        if "<html>" in data:  # No data
            return
        data = data.splitlines()

        # Header
        header = data.pop(0)
        assert header.count(";") == 7  # make sure it is acutally a header

        compiled_regex = re.compile(r"^(.*?)\((.*?)\)$")
        scheme_type = None
        scheme_subtype = None
        fund_name = None

        for line in data:
            if ";" in line:
                assert (
                    scheme_type is not None and scheme_subtype is not None and fund_name is not None
                )
                values = line.split(";")
                self.convert_dtypes(values)
                row = {
                    "scheme_type": scheme_type,
                    "scheme_subtype": scheme_subtype,
                    "fund_name": fund_name,
                    "scheme_code": values[0],
                    "scheme_name": values[1],
                    "isin_payout": values[2],
                    "isin_reinvestment": values[3],
                    "net_asset_value": values[4],
                    "repurchase_price": values[5],
                    "sale_price": values[6],
                    "nav_date": values[7],
                }
                yield row
            else:
                match = compiled_regex.match(line)
                if match:
                    scheme_type, scheme_subtype = (s.strip() for s in match.groups())
                else:
                    fund_name = line.strip()
