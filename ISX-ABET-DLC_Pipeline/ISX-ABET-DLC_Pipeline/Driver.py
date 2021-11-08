from ExtractionUtilities import ExtractionUtilities


class Driver:
    def main():
        pass

    def ask_single_or_multiple_vids(
        option_1: str, option_2: str
    ) -> ExtractionUtilities:
        number_to_preprocess = input(
            "Would you you like to preprocess one vid or mulitple vids?"
        )

        if number_to_preprocess.str.contains("one"):
            ExtractionUtilities.preprocess_single_vid()
        elif number_to_preprocess.str.contains("multiple"):
            ExtractionUtilities.preprocess_multiple_vids()
        else:
            print("Please choose a valid option!")
            print("Your input must either contain %s or %s." % (option_1, option_2))


if __name__ == "__main__":
    Driver.main()
