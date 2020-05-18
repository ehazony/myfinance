from os import path

from myFinance.models import Tag


class TagDb:
    def __init__(self, dirr):
        self.files_dir = dirr
        assert path.exists(dirr), "directory for db dose not exist"
        self.tagged_lists = self.get_tagged_lists()

    def get_tagged_lists(self, errase_duplicets=False):
        """
        :returns: dict, {file name: [transaction names]}
        """
        data = dict()
        for file_name in tags_file_names:
            try:
                with open(self.files_dir + "\\" + file_name, 'r', encoding='utf-8') as f:
                    content = f.readlines()
            except:
                with  open(self.files_dir + "\\" + file_name, 'w+', encoding='utf-8') as f:
                    content = []

            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content]
            content = list(dict.fromkeys(content))
            data[file_name] = content
            f.close()
            if errase_duplicets:
                # errase duplicets
                with open(self.files_dir + "\\" + file_name, "w", encoding='utf-8') as f:
                    f.writelines(["%s\n" % item for item in data[file_name]])

        return data

    def save_transaction_name(self, file_name, transaction_name):
        self.tagged_lists[file_name].append(transaction_name)
        with open(self.files_dir + "\\" + file_name, "a", encoding='utf-8') as f:
            f.write("%s\n" % transaction_name)

    def get_file_that_contains(self, transaction_name):
        for tag in tags_file_names:
            if transaction_name in self.tagged_lists[tag]:
                return tag
        return None


all_tags = Tag.objects.all()
tags_names = [tag.name for tag in all_tags]
tags_file_names = [tag.file_name for tag in all_tags]
TAG_CHOICES = [(tag.replace(".txt", ""), tag.replace(".txt", "")) for tag in tags_file_names]