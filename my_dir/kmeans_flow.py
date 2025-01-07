from metaflow import FlowSpec, step, Parameter, resources, conda_base, profile

@conda_base(python='3.8.3', libraries={'scikit-learn': '0.24.1'})  #A
class KmeansFlow(FlowSpec):

    num_docs = Parameter('num-docs', help='Number of documents', default=1000000)

    @resources(memory=4000)  #B
    @step
    def start(self):
        import scale_data  #C
        docs = scale_data.load_yelp_reviews(self.num_docs)  #C
        self.mtx, self.cols = scale_data.make_matrix(docs)  #C
        print("matrix size: %d x %d" % self.mtx.shape)
        self.next(self.train_kmeans)

    @resources(cpu=16, memory=4000)  #D
    @step
    def train_kmeans(self):
        from sklearn.cluster import KMeans
        with profile('k-means'):  #E
            kmeans = KMeans(n_clusters=10,
                            verbose=1,
                            n_init=1)  #F
            kmeans.fit(self.mtx)  #F
            self.clusters = kmeans.labels_  #F
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == '__main__':
    KmeansFlow()
