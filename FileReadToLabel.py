class LabelProcessor:
    """
    Yalnızca aldığı parametreler ile işlem yapıyorsa
    @staticmethod kullanılıyor
    """
    @staticmethod
    def read_labels_from_file(file_path):
        if not file_path.endswith('.txt'):
            raise ValueError(f"Expected a .txt file, but got {file_path}")
        labels = []
        with open(file_path, 'r',encoding='ISO-8859-1') as file:
            for line in file:
                values = line.strip().split()
                label_class = int(values[0])
                x_center = float(values[1])
                y_center = float(values[2])
                width = float(values[3])
                height = float(values[4])
                labels.append([label_class, x_center, y_center, width, height])
        return labels

    @staticmethod
    def write_labels_to_file(file_path, labels):
        with open(file_path, 'w') as file:
            for label in labels:
                class_id, x_center, y_center, width, height = label
                x_center = x_center + 1 if x_center < 0 else x_center
                y_center = y_center + 1 if y_center < 0 else y_center
                file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")