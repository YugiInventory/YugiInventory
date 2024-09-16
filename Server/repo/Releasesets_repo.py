from .repository_interface import ReadOnlyRepositoryInterface
from models import ReleaseSet

class ReleaseSetsRepository(ReadOnlyRepositoryInterface):
    search_filters = {
        'releaseDate_exact' : '',
        'releaseDate_less_than' : '',
        'releaseDate_greater_than' : '',
        'name_exact' : '',
        'name_partial' : lambda value: ReleaseSet.name.ilike(f'%{value}%'),
        'setCode_partial' : lambda value: ReleaseSet.set_code.ilike(f'%{value}%')
    }

    def get_releaseSet_detailed(self,filters):
        #Same query as get, but we get joined card info. I really should look at the models first to fix this issue with unnecessary queries
        pass

    def __init__(self):
        super().__init__(ReleaseSet)