from flask import Blueprint, request, jsonify
from Backend.pipeline import documentation_pipeline

bp = Blueprint("routes", __name__)

@bp.route("/query-documentation", methods=["POST"])
def query_documentation():
    """
    Endpoint to query documentation.
    Expects JSON payload with 'url' and 'question'.
    """
    try:
        # Parse input JSON
        data = request.json
        print(data)
        url = data.get("url")
        question = data.get("question")

        if not url or not question:
            return jsonify({"error": "Both 'url' and 'question' are required."}), 400

        # Run the pipeline
        response = documentation_pipeline(url, question)

        #return jsonify({"response": response})
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500
