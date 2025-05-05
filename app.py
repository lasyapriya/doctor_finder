from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import papermill as pm
import pandas as pd
import pickle
import os
import shutil
import logging

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# --- Load Data ---
def load_data():
    df = pd.read_excel("panel_data.xlsx", parse_dates=False)
    return df

df = load_data()
specialities = df['Speciality'].unique()
regions = ['All Regions'] + list(df['Region'].unique())

@app.route('/')
def index():
    return render_template('index.html', specialities=specialities, regions=regions)

@app.route('/search', methods=['POST'])
def search():
    speciality = request.form.get('speciality')
    region = request.form.get('region')
    logger.debug(f"Received speciality: {speciality}, region: {region}")

    # Sanitize speciality and region for filenames
    speciality_safe = speciality.replace(" ", "_").lower()
    region_safe = region.replace(" ", "_").lower() if region != 'All Regions' else "all_regions"
    logger.debug(f"Sanitized speciality: {speciality_safe}, region: {region_safe}")

    # Prepare parameters for the notebook execution
    params = {"speciality": speciality, "region": region if region != 'All Regions' else "All_Regions"}
    
    try:
        # Execute the notebook with papermill
        pm.execute_notebook("test2.ipynb", "output.ipynb", parameters=params, kernel_name="python3")
        logger.debug("Notebook executed successfully")
    except Exception as e:
        logger.error(f"Error executing notebook: {str(e)}")
        return jsonify({"error": f"Error executing notebook: {str(e)}"}), 500

    try:
        # Load the output of the notebook
        with open('output.pkl', 'rb') as f:
            regions_df_list, region_names = pickle.load(f)
        logger.debug("Successfully loaded output.pkl")
    except FileNotFoundError:
        logger.error("Output file 'output.pkl' not found")
        return jsonify({"error": "Output file 'output.pkl' not found."}), 500

    # Render the results
    results = []
    for region_df, region_name in zip(regions_df_list, region_names):
        if not region_df.empty:
            region_result = {
                'region_name': region_name,
                'data': region_df[['NPI', 'State', 'Usage Time (mins)', 'Region', 'Speciality']].to_dict(orient='records')
            }
            results.append(region_result)

    # Create static/plots directory if it doesn't exist
    os.makedirs("static/plots", exist_ok=True)

    # Define plot files (match the notebook's naming convention)
   # In app.py, update the plot_files list
    plot_files = [
    f'plots/region_counts_{speciality_safe}_{region_safe}.png',
    f'plots/state_counts_{speciality_safe}_{region_safe}.png',
    f'plots/avg_usage_by_state_{speciality_safe}_{region_safe}.png',
    f'plots/usage_time_dist_{speciality_safe}_{region_safe}.png',
    f'plots/usage_time_boxplot_{speciality_safe}_{region_safe}.png',
    f'plots/heatmap_{speciality_safe}_{region_safe}.png',
    f'plots/top_states_avg_usage_{speciality_safe}_{region_safe}.png',
    f'plots/pie_state_dist_{speciality_safe}_{region_safe}.png',
    f'plots/usage_threshold_{speciality_safe}_{region_safe}.png',
    f'plots/top_npis_{speciality_safe}_{region_safe}.png'
]
    logger.debug(f"Expected plot files: {plot_files}")

    # Copy plots to static/plots/
    for plot_file in plot_files:
        plot_name = os.path.basename(plot_file)
        src = plot_file
        dst = f"static/plots/{plot_name}"
        if os.path.exists(src):
            shutil.copy(src, dst)
            logger.debug(f"Copied {src} to {dst}")
        else:
            logger.warning(f"Plot file {src} not found")

    # Generate plot URLs
    plot_urls = [f"/static/plots/{os.path.basename(plot_file)}" for plot_file in plot_files if os.path.exists(f"static/plots/{os.path.basename(plot_file)}")]
    logger.debug(f"Generated plot URLs: {plot_urls}")

    return render_template('results.html', results=results, plot_urls=plot_urls)

if __name__ == '__main__':
    app.run(debug=True)
