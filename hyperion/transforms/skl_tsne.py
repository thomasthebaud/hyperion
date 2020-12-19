"""
 Copyright 2018 Johns Hopkins University  (Author: Jesus Villalba)
 Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)
"""
import numpy as np
import h5py

from sklearn.manifold import TSNE

from ..hyp_model import HypModel

class SklTSNE(HypModel):
    """Wrapper class for sklearn TSNE manifold learner

    Attributes:
      tsne_dim: dimension of the embedded space.
      perplexity: the perplexity is related to the number of nearest neighbors that is used in other manifold learning algorithms. Larger datasets usually require a larger perplexity. Consider selecting a value between 5 and 50. 
      early_exaggeration: controls how tight natural clusters in the original space are in the embedded space and how much space will be between them. 
      lr: the learning rate for t-SNE is usually in the range [10.0, 1000.0]. 
      num_iter: maximum number of iterations for the optimization.
      num_iter_without_progress: maximum number of iterations without progress before we abort the optimization
      min_grad_norm: if the gradient norm is below this threshold, the optimization will be stopped.
      metric: the metric to use when calculating distance between instances in ['cosine', 'euclidean', 'l1', 'l2', 'precomputed'] or callable function.
      init: initialization method in ['random', 'pca'] or embedding matrix of shape (num_samples, num_comp)
      verbose: verbosity level.
      rng: RandomState instance
      rng_seed: seed for random number generator
      method: gradient calculation method in [‘barnes_hut’, 'exact']
      angle: angle thetha in Barnes-Hut TSNE
      num_jobs: number of parallel jobs to run for neighbors search.
    """
    def __init__(self, tsne_dim=2, perplexity=30.0, early_exaggeration=12.0, 
                 lr=200.0, num_iter=1000, num_iter_without_progress=300, 
                 min_grad_norm=1e-07, metric='euclidean', init='random', 
                 verbose=0, rng=None, rng_seed=1234, method='barnes_hut', 
                 angle=0.5, num_jobs=None, **kwargs):

        super().__init__(**kwargs)
        self.rng_seed = rng_seed
        if rng is None:
            rng = np.random.RandomState(seed=rng_seed)

        self._tsne = TSNE(
            n_components=tsne_dim, perplexity=perplexity, 
            early_exaggeration=early_exaggeration, 
            learning_rate=lr, n_iter=num_iter, 
            n_iter_without_progress=num_iter_without_progress, 
            min_grad_norm=min_grad_norm, metric=metric, init=init, 
            verbose=verbose, random_state=rng, method=method, 
            angle=angle, n_jobs=num_jobs)

    @property
    def tsne_dim(self):
        return self._tsne.n_components

    @property
    def perplexity(self):
        return self.perplexity

    @property
    def early_exaggeration(self):
        return self._tsne.early_exaggeration

    @property
    def lr(self):
        return self._tsne.learning_rate

    @property
    def num_iter(self):
        return self._tsne.n_iter

    @property
    def num_iter_without_progress(self):
        return self._tsne.n_iter_without_progress

    @property
    def min_grad_norm(self): 
        return self._tsne.min_grad_norm

    @property
    def metric(self):
        return self._tsne.metric

    @property
    def init(self):
        return self._tsne.init

    @property
    def method(self):
        return self._tsne.method

    @property
    def angle(self):
        return self._tsne.angle

    @property
    def num_jobs(self):
        return self._tsne.n_jobs


    def predict(self, x):
        return self._tsne.fit_transform(x)

    def fit(self, x):
        return self._tsne.fit_transform(x)


    def save_params(self, f):
        pass
        
    @classmethod
    def load_params(cls, f, config):
        return cls(**config)

    def get_config(self):
        config = {'tsne_dim': self.tsne_dim,
                  'perplexity': self.perplexity,
                  'early_exaggeration': self.early_exaggeration,
                  'lr': self.lr,
                  'num_iter': self.num_iter, 
                  'num_iter_without_progress': self.num_iter_without_progress,
                  'min_grad_norm': self.min_grad_norm,
                  'metric': self.metric,
                  'init': self.init,
                  'rng_seed': self.rng_seed,
                  'method': self.method,
                  'angle': self.angle,
                  'num_jobs': self.num_jobs}
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))


    @staticmethod
    def filter_args(prefix=None, **kwargs):
        if prefix is None:
            p = ''
        else:
            p = prefix + '_'
            
        valid_args = ('tsne_dim', 'perplexity', 'early_exaggeration', 'lr', 
                      'num_iter', 'num_iter_without_progress', 
                      'min_grad_norm', 'metric',
                      'init', 'rng_seed', 'method', 'angle', 'num_jobs')
        return dict((k, kwargs[p+k])
                    for k in valid_args if p+k in kwargs)

    
    @staticmethod
    def add_argparse_args(parser, prefix=None):
        if prefix is None:
            p1 = '--'
            p2 = ''
        else:
            p1 = '--' + prefix + '-'
            p2 = prefix + '_'
            
        parser.add_argument(p1+'tsne-dim', default=2, type=int,
                            help=('tsne dimension'))

        parser.add_argument(p1+'perplexity', default=30., type=float,
                            help=('tsne perplexity'))
        parser.add_argument(
            p1+'early-exaggeration', default=12., type=float,
            help=('controls how tight natural clusters in the original space' 
                  'are in the embedded space and how much space will be '
                  'between them.'))
        parser.add_argument(p1+'lr', default=200., type=float,
                            help=('learning rate for t-sne'))
        parser.add_argument(p1+'num-iter', default=1000, type=int,
                            help=('max. number of iterations'))
        parser.add_argument(p1+'num-iter-without-progress', default=300, type=int,
                            help=('max. number of iterations without improvement'))
        parser.add_argument(p1+'min-grad-norm', default=1e-07, type=float,
                            help=('minimum gradient norm to stop optim.'))
        parser.add_argument(p1+'metric', default='euclidean',
                            choices=['cosine', 'euclidean', 'l1', 'l2', 'precomputed'],
                            help=('distance metric'))
        parser.add_argument(p1+'init', default='random',
                            choices=['random', 'pca'],
                            help=('initialization method'))
        parser.add_argument(p1+'method', default='barnes_hut',
                            choices=['barnes_hut', 'exact'],
                            help=('gradient calculation method'))
        parser.add_argument(p1+'angle', default=0.5, type=float,
                            help=('angle thetha in Barnes-Hut TSNE'))
        parser.add_argument(p1+'num-jobs', default=1, type=int,
                            help=('num parallel jobs for NN search'))
        parser.add_argument(p1+'rnd-seed', default=1234, type=int,
                            help=('random seed'))
        
