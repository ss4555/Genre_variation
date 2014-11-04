from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import csv
import os
# Create your views here.

def index(request):
    context = {"test":[1,2,3,4]}
    return render(request, 'masc/index.html',context)

def read_csv(request):
    if request.method == 'POST':
        transform_matrix = []
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, "data/coefforth.txt")


### open the file that contains the transform matrix
        with open(file_path) as transform_matrix_file:
            for row in transform_matrix_file.readlines():
                transform_matrix.append([float(x) for x in row.strip().split(" ")])

### open the csv file that the clients uploaded
        reader = csv.reader(request.FILES['uploadfile'])
        next(reader,None) # returns the headers or `None` if the input is empty
        original_score = []
        for row in reader:
            # row[1:-3] is for the specific file format that I have now
            original_score.append([float(x) for x in row[1:-2]])

### normalize the data
    ## open the mean and std file
        mean_file_path = os.path.join(module_dir, "data/mean.txt")
        mean = []
        with open(mean_file_path) as mean_file:
            mean = [float(x) for x in mean_file.readline().strip().split(" ")]
        std_file_path = os.path.join(module_dir, "data/std.txt")
        std = []
        with open(std_file_path) as std_file:
            std = [float(x) for x in std_file.readline().strip().split(" ")]
    ## compute the normalized data
        for row in original_score:
            for i in range(len(row)):
                row[i] = (row[i]-mean[i])/std[i]

### matrix multiplication
        # original_score: n of files * k of features
        # transform matrix: k of features * m component
        result = []
        for n in range(len(original_score)):
            result.append([])
            for m in range(len(transform_matrix[0])):
                result[n].append(0)
                for k in range(len(original_score[0])):
                    result[n][m] += original_score[n][k]*transform_matrix[k][m]
            print result[n]

### render the result
    genres = []
    graph1 = []
    graph2 = []
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, "data/genre_nums.txt")
    with open(file_path) as ff:
        for line in ff.readlines():
            genres.append(int(line.strip()))
    file_path = os.path.join(module_dir, "data/cscores.txt")
    with open(file_path) as ff:
        for line in ff.readlines():
            temp = [float(x) for x in line.strip().split(" ")]
            assert len(temp) == 4
            graph1.append(temp[0:2])
            graph2.append(temp[2:])
    context = {"genres": genres,
               "graph1": graph1,
               "graph2": graph2,
               "graph3": [ele[0:2] for ele in result],
               "graph4": [ele[2:] for ele in result]}
    return render(request,'masc/render_origin_graph.html',context)



def render_model_graph(request,result):
    """pass two data sets
    # first is genre
    # the others is graph1 and graph2
    """
    genres = []
    graph1 = []
    graph2 = []
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, "data/genre_nums.txt")
    with open(file_path) as ff:
        for line in ff.readlines():
            genres.append(int(line.strip()))
    file_path = os.path.join(module_dir, "data/cscores.txt")
    with open(file_path) as ff:
        for line in ff.readlines():
            temp = [float(x) for x in line.strip().split(" ")]
            assert len(temp) == 4
            graph1.append(temp[0:2])
            graph2.append(temp[2:])
    context = {"genres": genres, "graph1": graph1, "graph2": graph2, "graph3": result}
    return render(request,'masc/render_origin_graph.html',context)



