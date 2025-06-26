## How to run

- Create environment variable
    - Go to System → Advanced system settings → Environment Variables
    - Under ```User variables``` or ```System variables```, click New
    - ```Name: REPO_PYSCRIPT, Value: {path_to_local_repository}```


- Go to Steam → Manage → Properties → General and add the next line to **_launch options_**:
```"{path_to_local_repository}\launch_repo.bat" %command%```. For example: ```"C:\repo-saves-synchronizer\launch_repo.bat" %command%```


## Notes

- The file ```repo_copy.log``` is created in the steam directory, namely in the directory where the game was installed
