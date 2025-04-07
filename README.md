# codemigratorai

Step1: Open anaconda power shell and go to your project directory and run 
conda env create -f environment.yml
conda activate angular-migrator

Step 2: 
Run below command to convert from Angular lower version to a higher version. If you are migrating to Angular 16 or above it is going to generate standalone components. Passing anthropic key is option. Alternatively you can setup .env and add ANTHROPIC_API_KEY or OPENAAI_API_KEY
--config is used for any project related dependencies
python angular_migrator.py --src /path/to/angularjs --out /path/to/output --api-key your-anthropic-api-key --config your-config.json 

Tried converting angular6 to angular 16 using sample project. original-files contains code which needed to be modified. AI generated @if in html code which is only available from Angular 17 and created modules file which is redundant.
