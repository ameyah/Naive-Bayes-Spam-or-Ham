import argparse
import os

__author__ = 'ameya'


class BayesClassify():
    class __BayesClassify():
        def __init__(self):
            self.classify_dir = None
            self.prob_spam = 0
            self.prob_ham = 0

            self.spam_dirs = []
            self.ham_dirs = []
            self.total_files = 0
            self.spam_files = 0
            self.ham_files = 0
            self.train_data = dict()
            self.spam_words = 0
            self.ham_words = 0

        def set_classify_dir(self, classify_dir):
            self.classify_dir = classify_dir

        def cache_training_model(self, model_file):
            with open(model_file, 'r', encoding='latin1') as file_handler:
                prob_spam_line = file_handler.readline()
                self.prob_spam = float(prob_spam_line)
                prob_ham_line = file_handler.readline()
                self.prob_ham = float(prob_ham_line)
                while True:
                    line = file_handler.readline()
                    if not line:
                        break
                    line_content = line.split()
                    if line_content[0] in self.train_data:
                        print("duplicate: " + str(line_content[0]))
                    else:
                        self.train_data[str(line_content[0])] = [float(line_content[1]), float(line_content[2])]

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
                    try:
                        file_handler.write(
                            str(token) + ' ' + str(self.train_data[token][0] / self.spam_words) + ' ' + str(
                                self.train_data[token][1] / self.ham_words) + '\n')
                    except:
                        print("exception in writing training data: " + str(token))
                        continue

    __instance = None

    def __init__(self):
        if BayesClassify.__instance is None:
            BayesClassify.__instance = BayesClassify.__BayesClassify()
        self.__dict__['BayesClassify__instance'] = BayesClassify.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)


def get_classify_dir():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help='Directory of input development data.')
    args = parser.parse_args()
    return args.input_dir


if __name__ == '__main__':
    classify_instance = BayesClassify()
    classify_instance.set_classify_dir(get_classify_dir())
    classify_instance.cache_training_model('nbmodel.txt')
    # classify_instance.map_spam_ham_dirs()
    # classify_instance.train_model()
    # classify_instance.write_training_data('nbmodel.txt')