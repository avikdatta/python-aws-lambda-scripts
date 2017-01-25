from __future__ import print_function
from collections import defaultdict

class FtpIndex:
 
  def __init__(self,infile):
    self.index=infile

  def get_all_stats(self):
    self.index_data=self._read_index_file()
    stats=dict()
    stats['Library_strategy']=self._get_count_stat('library_strategy')
    stats['Experiment_type']=self._get_count_stat('experiment_type')
    stats['Biomaterial_type']=self._get_count_stat('biomaterial_type')
    stats['Disease']=self._get_count_stat('disease')
    return stats

  def _get_count_stat(self, key):
    index_data=self.index_data
    key_dict=defaultdict(lambda: defaultdict(int))
    stats_dict=dict()
    
    try:
      for row in index_data:
        exp_id=row['experiment_id']
        key_val=row[key]
        
        if (key_val != '-') & (key_val != 'None'):
          key_dict[key_val][exp_id] +=1
        
      for key, val in key_dict.items():
         stats_dict[key]=len(val.keys())
      return stats_dict   
    
    except Exception as e:
      print('err1', e)
      raise SystemExit  

  def _read_index_file(self):
    '''
    Read an index file and a list of fields (optional)
    Returns a list of dictionary 
    '''

    infile=self.index

    try:
      with open(infile, 'r') as f:
        header=[]
        file_list=[]

        for i in f:
          row=i.strip().split("\t")
          if(header):
            filtered_dict=dict((k,v) for k,v in dict(zip(header,row)).items())
            file_list.append(filtered_dict)
          else:
            header=list(map(lambda x: x.lower(), row))
      return file_list
    except Exception as e:
      print('err2', e)
      raise SystemExit

