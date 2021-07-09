import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt

class pic_utils:
    """
    Read more in the 'github.com/lee-ju/PIC'

    Parameters
    ----------
    1. `from_cam`: In-node lists of Citation Adjacency Matrix.
    2. `to_cam`: Out-node lists of Citation Adjacency Matrix.
    3. `from_sam`: In-node lists of Similarity Adjacency Matrix.
    4. `to_sam`: Out-node lists of Similarity Adjacency Matrix.
    5. `repo`: Dictionary of apps and apps_date.
    6. `direct`: Boolean controlling the DiGraph. (default: True)
    """
    def __init__(self, from_cam, to_cam, from_sam, to_sam, repo, direct=True):
        self.from_cam = from_cam
        self.to_cam = to_cam
        self.from_sam = from_sam
        self.to_sam = to_sam
        self.repo = repo
        self.direct = direct

        self.pic_E = []
        self.pic_L = []

        if self.direct:
            self.CS_net = nx.DiGraph()
            
        else:
            self.CS_net = nx.DiGraph()

    def explorer(self, max_date=20):
        """
        Read more in the 'github.com/lee-ju/PIC'
    
        Parameters
        ----------
        1. `max_date`: The maximum value of the time difference between the filing of two patents. (default: 20)
        """
        self.max_date = int(max_date)

        for i in tqdm(range(len(self.from_sam))):
            from_date = self.repo[self.from_sam[i]]
            to_date = self.repo[self.to_sam[i]]
            diff_date = from_date - to_date

            if abs(diff_date) <= self.max_date:
                if diff_date <= 0:
                    E = self.from_sam[i]
                    L = self.to_sam[i]

                else:
                    E = self.to_sam[i]
                    L = self.from_sam[i]

                idx_E = [e for e, value in enumerate(
                    self.from_cam) if value == E]

                # if (E, L) in CAM, they are not pic
                chk = 0
                for idx_e in idx_E:
                    if self.to_cam[idx_e] == L:
                        chk += 1
                        break
                    else:
                        pass
                    
                if chk == 0:
                    F1 = [self.to_cam[f] for f in idx_E]

                    for h in F1:
                        idx_F1 = [e for e, value in enumerate(
                            self.from_cam) if value == h]
                        F2 = [self.to_cam[f] for f in idx_F1]

                        if len(F2) != 0:
                            for k in F2:
                                if k == L:
                                    self.pic_E.append(E)
                                    self.pic_L.append(L)
                else:
                    # (E, L) in CAM
                    pass
            else:
                # diff_date > max_date
                pass
            
        d = {'P_E': self.pic_E, 'P_L': self.pic_L}
        return_df = pd.DataFrame(d)
        return_df_dupdrop = return_df.drop_duplicates()
        return_pic_E = return_df_dupdrop['P_E']
        return_pic_L = return_df_dupdrop['P_L']

        return return_pic_E, return_pic_L

    def cs_net(self, pic_E, pic_L, fs=[10, 10], with_labels=True,
               node_size=300, font_size=12, seed=10):
        """
        Read more in the 'github.com/lee-ju/PIC'
    
        Parameters
        ----------
        1. `pic_E`: Output of pic_utils.explorer (CS-Net  on [PIC](https://doi.org/10.3390/su13020820)).
        2. `fs`: List of figsize=[horizontal_size, vertical_size]. (default: [10, 10])
        3. `with_labels`: Boolean controlling the use of node labels. (default: True)
        4. `node_size`: Size of nodes. (default: 100)
        5. `font_size`: Size of labels. (default: 12)
        6. `seed`: Seed for random visualization. (default: 10)
        """
        self.pic_E = pic_E
        self.pic_L = pic_L

        self.fs = fs
        self.with_labels = with_labels
        self.node_size = int(node_size)
        self.font_size = int(font_size)
        self.seed = int(seed)

        for m in range(len(self.from_cam)):
            self.CS_net.add_nodes_from(
                [self.from_cam[m], self.to_cam[m]], color='white')
            self.CS_net.add_edge(
                self.from_cam[m], self.to_cam[m], color='black')
            
        for n in range(len(self.pic_E)):
            self.CS_net.add_nodes_from(
                [self.pic_E[n], self.pic_L[n]], color='#FF1744')
            self.CS_net.add_edge(self.pic_E[n], self.pic_L[n], color='#FF1744')
            
        node_color = nx.get_node_attributes(self.CS_net, 'color').values()
        edge_color = nx.get_edge_attributes(self.CS_net, 'color').values()

        plt.figure(figsize=(self.fs[0], self.fs[1]))
        pos = nx.spring_layout(self.CS_net, seed=self.seed)

        nx.draw(self.CS_net, pos=pos, with_labels=self.with_labels,
                node_color=node_color, edge_color=edge_color,
                font_size=self.font_size, node_size=self.node_size,
                alpha=0.8, width=0.5)
        
        ax = plt.gca()
        ax.collections[0].set_edgecolor('#000000')
        plt.axis('off')
        plt.show()

        return self.CS_net


if __name__ == '__main__':
    import pandas as pd

    from_cam = ['A', 'B', 'B', 'C', 'C']
    to_cam = ['D', 'A', 'E', 'B', 'F']

    from_sam = ['A', 'B']
    to_sam = ['C', 'C']

    repo = {'A':2017, 'B':2010, 'C':2005}

    pu = pic_utils(from_cam, to_cam, from_sam, to_sam, repo, direct=True)
    
    pic_E, pic_L = pu.explorer(max_date=20)
    pic = {'P_E': pic_E, 'P_L': pic_L}
    
    df_pic = pd.DataFrame(pic)
    print(df_pic)

    CS_net = pu.cs_net(pic_E, pic_L, fs=[3, 3], with_labels=True,
                       node_size=300, font_size=12, seed=10)
