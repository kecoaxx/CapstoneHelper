from better_bing_image_downloader import downloader
import os
import shutil
from PIL import Image
import glob
import webp
import Augmentor


def counter(dir):
  """
    Counting how many files within a directory

    Args:
        dir (str): The path to be counted.
    """
  return len(os.listdir(dir))

def getSubfolders(base_dir = './'):
  """
    Getting all the subdirectory names from the base directory

    Args:
        base_dir (str): The path to the base directory.
    """
  arr = next(os.walk(base_dir))[1]
  return arr

def rename_files_with_folder_name(base_dir):
    """
    Rename all files in the specified directory and its subdirectories
    by adding the parent folder name as a prefix to the filename.
    
    Args:
        base_dir (str): The path to the base directory.
    """
    if not os.path.isdir(base_dir):
        raise ValueError(f"The specified path '{base_dir}' is not a valid directory.")
    
    for root, _, files in os.walk(base_dir):
        # Get the name of the current folder
        folder_name = os.path.basename(root)
        
        for file_name in files:
            # Construct the old and new file paths
            old_file_path = os.path.join(root, file_name)
            new_file_name = f"{folder_name}_{file_name}"
            new_file_path = os.path.join(root, new_file_name)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)

    print(f"All files in '{base_dir}' have been renamed to include their folder name as a prefix.")


def extract_all_from_subfolders(base_dir):
    """
    Extract all files and subfolders from subfolders in the specified directory
    and move them to the base directory.
    
    Args:
        base_dir (str): The path to the directory to process.
    """
    if not os.path.isdir(base_dir):
        raise ValueError(f"The specified path '{base_dir}' is not a valid directory.")
    
    # Iterate over all items in the base directory
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        
        if item == 'venv' and os.path.isdir(item_path):
            continue

        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Iterate through all files/subfolders in the directory
            for sub_item in os.listdir(item_path):
                sub_item_path = os.path.join(item_path, sub_item)
                
                # Move each file/subfolder to the base directory
                shutil.move(sub_item_path, base_dir)
            
            # Remove the now-empty folder
            os.rmdir(item_path)

    total = len(os.listdir(base_dir))
    print(f"All items from subfolders in '{base_dir}' have been extracted to the base directory. total files in the folder are {total}")

def imageDownloader(query, route='./', limit=15):
  """
    Downloading images from Bing Images using Better bing image downloader.
    
    Args:
        query (list): queries for the images to be downloaded
        route (str): the route to be used to download the images
        limit (int): the number of images to be downloaded
    """
  
  altered_query = []
  
  for i in query:
    y = i + ' products photos'
    altered_query.append(y)
  
  print(altered_query)
  
  for i in altered_query:
      
      # Call the downloader with the correct query format
      downloader(i, limit=limit, output_dir=route, adult_filter_off=True,
      force_replace=False, timeout=60, filter="photo", verbose=True, badsites=[], name=i)
      
      print('Downloaded images for query: ', i)
      
      
def extentions_checkers(base_dir = './'):
  """
    Returns unique extentions of the given base directory
    
    Args:
        base_dir (str): The path to the base directory. default is './'
    """
  extensions = set()
  my_root = base_dir  # some dir to start in

  for root, dirs, files in os.walk(my_root) :
      for file in files: 
          pathname, exten = os.path.splitext(file) 
          extensions.add(exten)
          
  result = list(extensions)

  return result


def image_type_converter(base_dir, imgtype = 'jpeg'):
  """
    Convert all sorts of images type into a single type of user choice
    
    Args:
        base_dir (str): The path to the base directory.
        imgtype (str): The desired image type. Default is 'jpeg'.
    """
  datatypes = extentions_checkers(base_dir)
  if imgtype in datatypes:
    datatypes.remove(f'.{imgtype}')
  notSupportedFiles = [] 
  unsupportedExtensions = set()
  
  
  for datatype in datatypes:
    print(f'on {datatype} rn ==============================================')
    for infile in glob.glob(f"{base_dir}/*{datatype}"):
      file, ext = os.path.splitext(infile)
      try:
        if datatypes == '.webp':
          with webp.load_image(infile).convert('RGB') as img:
            img.save(f'{file}.{imgtype}', imgtype)
            print(f'Success saving {file}.{imgtype}')
        else:
          with Image.open(infile) as img:
            if img.mode != 'RGB':
              img = img.convert('RGB')
            img.save(f'{file}.{imgtype}', imgtype)
            print(f'Success saving {file}.{imgtype}')
      except Exception as e:
                print(f"Failed to process {infile}: {e}")
                notSupportedFiles.append(infile)
                pathname, exten = os.path.splitext(file) 
                unsupportedExtensions.add(exten)
      os.remove(infile)
      print(f'deleted {infile}')
                
  notSupportedFilesCount = len(notSupportedFiles)
  if notSupportedFilesCount != 0:
    userInput = input(f'there are {notSupportedFilesCount} unsupported files that consists of {list(unsupportedExtensions)}, want to delete them? (y/n): ')
    if userInput.lower() == 'y':
      for file in notSupportedFiles:
        os.remove(file)
        print(f'deleted {file}')
    else:
      print('files are not deleted')
  
  print('done hehe')

def augmenters(path, sample):
  """
    Augment images

    Args:
        path (str): The path to the image directory.
        sample (int): how many outputs of augmented images are needed.
    """
  if type(sample) != int:
    print('sample is not an integer')
    return None
  if not os.path.exists(path):
    print("path doesn't exist")
    return None

  p = Augmentor.Pipeline(path)
  p.flip_left_right(0.5)
  p.black_and_white(0.1)
  p.rotate(0.3, 10, 10)
  p.skew(0.4, 0.5)
  p.zoom(probability = 0.2, min_factor = 1.1, max_factor = 1.5)
  p.sample(sample)

if __name__ == '__main__':
  
 #codes here
 a = 1 + 1

imageDownloader(['tomato'], './images', 3)