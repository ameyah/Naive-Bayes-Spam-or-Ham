import argparse
import os

__author__ = 'ameya'


class BayesLearn():
    class __BayesLearn():
        def __init__(self):
            self.training_dir = None
            self.spam_dirs = []
            self.ham_dirs = []
            self.total_files = 0
            self.spam_files = 0
            self.ham_files = 0
            self.train_data = dict()
            self.spam_words = 0
            self.ham_words = 0

        def set_training_dir(self, training_dir):
            self.training_dir = training_dir

        # procedure to recursively determine all the spam and ham directories
        # and store in spam_dirs and ham_dirs
        def map_spam_ham_dirs(self):
            for current_dir, dirnames, filenames in os.walk(self.training_dir):
                last_dir_name = os.path.basename(current_dir)
                if last_dir_name == "spam":
                    self.total_files += len(filenames)
                    self.spam_files += len(filenames)
                    self.spam_dirs.append(current_dir)
                elif last_dir_name == "ham":
                    self.total_files += len(filenames)
                    self.ham_files += len(filenames)
                    self.ham_dirs.append(current_dir)

        def train_model(self):
            self.train_spam(self.spam_dirs, "spam")
            self.train_spam(self.ham_dirs, "ham")

        def train_spam(self, type_dir, type_mail):
            for single_dir in type_dir:
                for file_name in os.listdir(single_dir):
                    file_extension = os.path.splitext(file_name)[1]
                    if file_extension != '.txt':
                        continue
                    with open(os.path.join(single_dir, file_name), "r", encoding="latin1") as file_handler:
                        file_content = file_handler.read()
                        tokens = file_content.split()
                        for token in tokens:
                            if type_mail == "spam":
                                self.spam_words += 1
                            elif type_mail == "ham":
                                self.ham_words += 1
                            if token in self.train_data:
                                if type_mail == "spam":
                                    self.train_data[token.strip()][0] += 1
                                elif type_mail == "ham":
                                    self.train_data[token.strip()][1] += 1
                            else:
                                if type_mail == "spam":
                                    self.train_data[token.strip()] = [1, 0]
                                elif type_mail == "ham":
                                    self.train_data[token.strip()] = [0, 1]

        def write_training_data(self, write_file):
            with open(write_file, "w", encoding='latin1') as file_handler:
                # The first 2 lines are probabilities of spam and ham respectively
                file_handler.write(str(self.spam_files / self.total_files) + '\n')
                file_handler.write(str(self.ham_files / self.total_files) + '\n')
                # Rest of the lines are words followed by their probabilities given spam and ham separated by spaces
                for token in self.train_data:
                    file_handler.write(str(token) + ' ' + str(self.train_data[token][0] / self.spam_words) + ' ' + str(
                        self.train_data[token][1] / self.ham_words) + '\n')

    __instance = None

    def __init__(self):
        if BayesLearn.__instance is None:
            BayesLearn.__instance = BayesLearn.__BayesLearn()
        self.__dict__['BayesLearn__instance'] = BayesLearn.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)


def get_training_dir():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help='Directory of input training data.')
    args = parser.parse_args()
    return args.input_dir


if __name__ == '__main__':
    train_instance = BayesLearn()
    train_instance.set_training_dir(get_training_dir())
    train_instance.map_spam_ham_dirs()
    train_instance.train_model()
    train_instance.write_training_data('nbmodel.txt')