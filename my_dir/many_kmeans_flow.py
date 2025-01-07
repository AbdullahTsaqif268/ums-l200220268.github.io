from metaflow import FlowSpec, step, Parameter, resources
from sklearn.cluster import KMeans
import scale_data
from analyze_kmeans import top_words

class ManyKmeansFlow(FlowSpec):
    num_docs = Parameter('num-docs', help='Number of documents', default=1000000)

    @resources(memory=4000)
    @step
    def start(self):
        docs = scale_data.load_yelp_reviews(self.num_docs)
        self.mtx, self.cols = scale_data.make_matrix(docs)
        self.k_params = list(range(5, 55, 5))  # Range of k values for KMeans
        self.next(self.train_kmeans, foreach='k_params')

    @resources(cpu=4, memory=4000)
    @step
    def train_kmeans(self):
        self.k = self.input
        kmeans = KMeans(n_clusters=self.k, verbose=1, n_init=1)
        kmeans.fit(self.mtx)
        self.clusters = kmeans.labels_
        self.next(self.analyze)

    @step
    def analyze(self):
        self.top = top_words(self.k, self.clusters, self.mtx, self.cols)
        self.next(self.join)

    @step
    def join(self, inputs):
        self.top = {inp.k: inp.top for inp in inputs}
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == '__main__':
    ManyKmeansFlow()
