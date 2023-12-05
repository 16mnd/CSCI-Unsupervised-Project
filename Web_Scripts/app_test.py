from flask import Flask, render_template, request
import heapq

app = Flask(__name__)

def abnormal_finder(g_enzyme):
    check = 'G'
    this = [i for i in g_enzyme if check not in i]
    return this

def G_CU_splitter(g_enzyme):
    new_list = []

    for string in g_enzyme:
        modified_string = ''
        for char in string:
            modified_string += char
            if (char in ('U', 'C')) and (string.index(char) != len(string)-1):
                modified_string += '-'

        new_list.append(modified_string)

    return new_list


def CU_G_splitter(CU_enzyme):
    new_list = []

    for string in CU_enzyme:
        modified_string = ''
        for char in string:
            modified_string += char
            if (char in ('G')) and (string.index(char) != len(string)-1):
                modified_string += '-'

        new_list.append(modified_string)

    return new_list


def finder(first, second):
    singles = []
    
    final=first+second
    for i in final:
        if i.find('-') == -1:
            singles.append(i)
    
    return singles


def path_finder(first, second, abnormal, start_end):
    paths = []
    end = ''
    for i in start_end:
        if i in abnormal[0]:  #could be potential problem
            end = end + i
            start_end.remove(i) 
    final=first+second
    for i in final:
        if i.find('-') != -1:
            paths.append(i)
        if paths[-1].split('-')[-1] ==end:
            paths[-1]= paths[-1]+'*'+start_end[0]
            
    
    
    return paths, end


def vertice_finder(first, second):
    vertices = []
    final = first+second
    for i in final:
        temp = i.split('-')
        temp.pop(len(temp)-1)
        if len(temp)>0:
            temp.pop(0)  
        
        vertices+=temp
    
    return vertices

def start_end_func(edges, vertices):
    this = edges
    for i in vertices:
        this.remove(i)
    
    return this

def creation(vertices, end, this, paths):
    final_vertices = [i for i in vertices if i != end] #actual vertices after removing end one
    size=len(final_vertices)
    matrix  = [[[] for _ in range(size) ] for _ in range(size)] #adjacency matrix
    for i,j in enumerate(final_vertices):
        this[j]=i
    total_edge_counter = 0
    x=0
    for i in paths:
        if ('*' not in i):
            curr = i.split('-')
            out = this[curr[0]]
            inward = this[curr[-1]]
            curr.remove(curr[0])
            curr.remove(curr[-1])
            if len(curr)==0:
                matrix[out][inward].append(str(x))
                total_edge_counter+=1
                x+=1
            elif len(curr) != 0:
                matrix[out][inward].append('-'.join(curr))
                total_edge_counter+=1
    
    
        elif('*' in i):
            curr = i.split('*')
            incoming=curr[-1]
            
            ind=curr[0].find('-')
            adding=curr[0][ind+1:]
            
            outgoing = curr[0].replace(end,'').replace('-','') #U is going to be the end.. so just pass end
            curr.remove(curr[-1])
            matrix[this[outgoing]][this[incoming]].append(adding)
            total_edge_counter+=1
            
    
    return final_vertices, matrix, total_edge_counter, this



def eulerian_finder(end, start_end, matrix, total_edge_counter, dicter):
    start_end=start_end[0]
    reverse = {value: key for key, value in dicter.items()}
    paths = []
    queue = [([dicter[start_end]], [], [])]
    
    while queue:
        node, path, edges = heapq.heappop(queue)
        if ((node[-1] == end) and (len(edges)==total_edge_counter)):
            paths.append(path)
            continue
        elif(node[-1]==end and (len(edges) != total_edge_counter)):
            continue
            
        path.append(reverse[node[-1]])
        
        for i, j in enumerate(matrix[node[-1]]):
            if len(j) != 0:
                for x in j:
                    if x not in edges and x != end:
                        new_node = node + [i]
                        new_path = path + [x]  # Append the edge first
                        new_edges = edges + [x]
                        heapq.heappush(queue, (new_node, new_path, new_edges))
                    elif x not in edges and x == end:
                        new_node = node + [x]
                        new_path = path + [x]  # Append the edge first
                        new_edges = edges + [x]
                        heapq.heappush(queue, (new_node, new_path, new_edges))
    return paths


def cleaner(paths):
    proper = []
    for i in paths:
        curr_path = ''
        for j in i:
            j=j.replace('-','')
            if j.isupper() and j.isalpha():
                curr_path += j
        proper.append(curr_path)
    return proper

def main(user_input_G, user_input_CU):
    
    split_input = user_input_G.split(', ')
    g_enzyme_split = [string.strip() for string in split_input]
    
    split_input = user_input_CU.split(', ')
    CU_enzyme_split = [string.strip() for string in split_input]
    
    abnormal_extendedBase = abnormal_finder(g_enzyme_split)
    G_then_UC_split  = G_CU_splitter(g_enzyme_split)
    UC_then_G_split = CU_G_splitter(CU_enzyme_split) 
    edge_cases = finder(G_then_UC_split, UC_then_G_split)
    vertices = vertice_finder(G_then_UC_split, UC_then_G_split) 
    start_end = start_end_func(edge_cases, vertices)                 
    paths, end = path_finder(G_then_UC_split, UC_then_G_split, abnormal_extendedBase, start_end) 
    final_vertices, matrix, total_edge_counter, dicter = creation(vertices, end, {}, paths)
    eulerian_paths = eulerian_finder(end, start_end, matrix, total_edge_counter, dicter)
    proper_paths  = cleaner(eulerian_paths)
    return proper_paths

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        string1 = request.form['string1']
        string2 = request.form['string2']
        processed_result = process_strings(string1, string2)
        return render_template('result.html', result=processed_result)
    return render_template('input.html')

def process_strings(string1, string2):
    result = main(string1, string2)  # Call your main function here with appropriate inputs
    return result

if __name__ == '__main__':
    app.run(debug=True)
