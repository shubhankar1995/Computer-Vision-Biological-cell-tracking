import matplotlib.pyplot as plt


def plot_image(figure_title, image, label):
    fig = plt.figure()
    fig.suptitle(figure_title)

    plt.imshow(image)
    plt.axis('off')
    plt.title(label)

    plt.savefig(f'results/{figure_title}', bbox_inches='tight', pad_inches=0)
    plt.show()
