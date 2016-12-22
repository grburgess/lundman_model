from astromodels import *
from astropy.table import Table
import numpy as np

def read_table(table_file, eta_list, save_name, model_name, data_cut=None):
    """
    Read in a text file of the energy (first column) and f_nu flux from the lundman model.
    It assumes the parameter is eta. The eta values are input independently (should not be in file)
    and must be in the same order as the columns. This will generate the table which can thne be passed
    around.


    :param table_file: the name of the file containing the data
    :param eta_list: the list of eta values with theordering of the columns in the data file
    :param save_name: name of the file to save
    :param model_name: name of the model
    :param data_cut: a value of the f_nu flux to cut the table at
    """
    table = Table.read(table_file,format='ascii')

    # assuming the first column is energy range

    energy_range = table['col1']


    # we need to sort the etas
    sort_idx = np.argsort(eta_list)

    eta = eta_list[sort_idx]



    

    # set up a data cut for a flux value
    
    cut = np.ones_like(energy_range, dtype=bool)

    if data_cut is not None:

        # we will not cut all enetires below a certain threshold 
        
        assert type(data_cut) == float, "data_cut must be a float!"
        
        for idx in sort_idx:

            column = idx+2

            f_nu = np.array(table[ 'col%d'%column ])
            
            tmp_cut = f_nu >= data_cut
            
            cut = np.logical_and(cut,tmp_cut) 


    # Start building the template

    temp_factory = TemplateModelFactory(save_name,
                                        model_name,
                                        energy_range[cut],
                                        ['eta'])

    temp_factory.define_parameter_grid('eta',eta)


    # we now will input the flux values either cut or uncut 
    
    for entry, idx in zip(eta,sort_idx):

        # need to skip over the energy column
        column = idx+2

        f_nu = np.array(table[ 'col%d'%column ])

        # convert to photon space
        f_ph = f_nu[cut]/energy_range[cut]

        # add the data for this parameter value

        temp_factory.add_interpolation_data(f_ph,eta=entry)

    # Store it
    temp_factory.save_data(overwrite=True)
        
    


    
    
