from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Replace this with your OpenAI API Key
openai.api_key = "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"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/search", methods=["GET", "POST"])
def generate_workout_plan():
    if request.method == "POST":
        # Extract form data
        gender = request.form.get("gender")
        age = request.form.get("age")
        weight = request.form.get("weight")
        medical_condition = request.form.get("medical_condition")
        workout_type = request.form.get("workout_type")
        dumbbells = request.form.get("dumbbells")
        kettlebells = request.form.get("kettlebells")
        pull_up_bar = request.form.get("pull_up_bar")
        bench = request.form.get("bench") 
        other_equipment = request.form.get("other")
        goal = request.form.get("goal")
        workout_time = request.form.get("workout_time")
        action = request.form.get("action")

        # Remove medical condition if it's 'N/A'
        if medical_condition == "N/A":
            medical_condition = None

        # Build the equipment portion of the prompt
        equipment_details = []

        if dumbbells == "yes":
            equipment_details.append("dumbbells")
        if kettlebells == "yes":
            equipment_details.append("kettlebells")
        if pull_up_bar == "yes" :
            equipment_details.append(f"pull-up bar")
        if bench == "yes":  # Add bench to the equipment list
            equipment_details.append("bench")
        if other_equipment:
            equipment_details.append(f"other equipment: {other_equipment}")

        equipment_str = ", ".join(equipment_details) if equipment_details else "no equipment"

        # Generate the workout plan prompt
        outline_prompt = (
    f"Create a structured workout plan for a {age}-year-old {gender} who weighs {weight}kg. "
    f"The goal of the workout is {goal}. The plan should last for {workout_time} minutes. "
    f"Include exercises based on the following available equipment: {equipment_str}. "
    f"Please provide the workout in a clear, structured format, with the following sections: "
    f"1) Warm-up (include duration and exercises), "
    f"2) Circuit Training (list exercises with duration, repetitions, and rest periods between each), "
    f"3) Cool Down (stretching exercises with duration). "
    f"Make sure to include tips on form and any necessary modifications for different fitness levels."
)
        if action == "generate_plan":
            # Generate the workout plan (mocked for now)
            workout_outline = generate_workout_outline(outline_prompt)
            return jsonify(workout_outline=workout_outline)

        elif action == "generate_form_tips":
            # Generate form tips (mocked for now)
            tips_prompt = (
                f"Provide proper Structured form and technique tips for common exercises in a {workout_type} "
                f"workout plan. Ensure the advice is suitable for a {gender} aged {age}."
                f"Please provide the workout in a clear, structured format like 1. for this exercise, 2 and so on"
            )
            form_tips = generate_workout_outline(tips_prompt)
            return jsonify(form_tips=form_tips)

        elif action == "generate_detailed_instructions":
            # Generate detailed workout instructions (mocked for now)
            detailed_prompt = (
                f"Provide detailed workout instructions for a {age}-year-old {gender} looking to {goal}, "
                f"with a {workout_time}-minute workout plan, considering available equipment: {equipment_str}."
                f"500 words"
            )
            detailed_workout = generate_workout_outline(detailed_prompt)
            return jsonify(detailed_workout=detailed_workout)

    # Render the search page for GET requests
    return render_template("search.html")

def generate_workout_outline(prompt):
    try:
        # Call the OpenAI API with a chat completion request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if needed
            messages=[
                {"role": "system", "content": "You are a helpful fitness assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,  # Limit response length
            temperature=0.7  # Adjust for creative outputs
        )
        # Extract and return the generated content
        return response['choices'][0]['message']['content'].strip()
    except openai.error.AuthenticationError:
        return "Error: Invalid OpenAI API key. Please check your API configuration."
    except openai.error.OpenAIError as e:
        return f"Error communicating with OpenAI: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@app.route('/workout')
def workout():
    return render_template('workout.html')

@app.route('/workout_plan')
def workout_plan():
    workout_type = request.args.get('type', 'default')
    experience = request.args.get('experience', 'beginner')  # Get user's experience level, default is beginner

    # Define workouts and recommendations for each experience level
    workouts = {
'upper_body': [
        {'exercise': 'Push-Ups', 'beginner': '3 sets of 10 reps', 'intermediate': '3 sets of 20 reps', 'expert': '4 sets of 25 reps'},
        {'exercise': 'Dumbbell Bench Press', 'beginner': '3 sets of 8 reps with 10 lbs', 'intermediate': '3 sets of 12 reps with 20 lbs', 'expert': '4 sets of 15 reps with 30 lbs'},
        {'exercise': 'Pull-Ups', 'beginner': '2 sets of 5 reps with assistance', 'intermediate': '3 sets of 10 reps', 'expert': '4 sets of 15 reps'},
        {'exercise': 'Shoulder Press', 'beginner': '3 sets of 8 reps with 10 lbs', 'intermediate': '3 sets of 12 reps with 20 lbs', 'expert': '4 sets of 15 reps with 25 lbs'},
    ],
    'cardio': [
        {'exercise': 'Running', 'beginner': '10 minutes at a slow pace', 'intermediate': '20 minutes at a moderate pace', 'expert': '30 minutes at a fast pace'},
        {'exercise': 'Cycling', 'beginner': '15 minutes at low resistance', 'intermediate': '25 minutes at medium resistance', 'expert': '40 minutes at high resistance'},
        {'exercise': 'Jump Rope', 'beginner': '3 sets of 1 minute', 'intermediate': '4 sets of 2 minutes', 'expert': '5 sets of 3 minutes'},
        {'exercise': 'Rowing', 'beginner': '10 minutes at a steady pace', 'intermediate': '20 minutes at moderate pace', 'expert': '30 minutes at fast pace'},
    ],
    'strength_training': [
        {'exercise': 'Deadlift', 'beginner': '3 sets of 5 reps with 20 lbs', 'intermediate': '3 sets of 8 reps with 50 lbs', 'expert': '4 sets of 10 reps with 100 lbs'},
        {'exercise': 'Squats', 'beginner': '3 sets of 8 reps with bodyweight', 'intermediate': '3 sets of 12 reps with 20 lbs', 'expert': '4 sets of 15 reps with 50 lbs'},
        {'exercise': 'Lunges', 'beginner': '3 sets of 8 reps per leg with bodyweight', 'intermediate': '3 sets of 10 reps per leg with 15 lbs', 'expert': '4 sets of 12 reps per leg with 25 lbs'},
        {'exercise': 'Leg Press', 'beginner': '3 sets of 8 reps with 50 lbs', 'intermediate': '3 sets of 10 reps with 100 lbs', 'expert': '4 sets of 12 reps with 150 lbs'},
    ],
    'flexibility': [
        {'exercise': 'Yoga', 'beginner': '15 minutes of basic poses', 'intermediate': '30 minutes of intermediate poses', 'expert': '45 minutes of advanced poses'},
        {'exercise': 'Stretching', 'beginner': '5 stretches held for 15 seconds each', 'intermediate': '10 stretches held for 20 seconds each', 'expert': '15 stretches held for 30 seconds each'},
        {'exercise': 'Hamstring Stretch', 'beginner': 'Hold for 20 seconds', 'intermediate': 'Hold for 30 seconds', 'expert': 'Hold for 45 seconds'},
        {'exercise': 'Hip Flexor Stretch', 'beginner': 'Hold for 20 seconds', 'intermediate': 'Hold for 30 seconds', 'expert': 'Hold for 45 seconds'},
    ],
    'full_body': [
        {'exercise': 'Burpees', 'beginner': '2 sets of 10 reps', 'intermediate': '3 sets of 15 reps', 'expert': '4 sets of 20 reps'},
        {'exercise': 'Mountain Climbers', 'beginner': '2 sets of 20 reps', 'intermediate': '3 sets of 30 reps', 'expert': '4 sets of 40 reps'},
        {'exercise': 'Jumping Jacks', 'beginner': '2 sets of 20 reps', 'intermediate': '3 sets of 30 reps', 'expert': '4 sets of 40 reps'},
        {'exercise': 'High Knees', 'beginner': '2 sets of 30 seconds', 'intermediate': '3 sets of 45 seconds', 'expert': '4 sets of 60 seconds'},
    ],
    }

    # Get workouts for the selected type
    selected_workouts = workouts.get(workout_type, [{'exercise': 'No workouts found for this category.'}])

    return render_template(
        'workout_plan.html',
        type=workout_type,
        workouts=selected_workouts,
        experience=experience
    )

if __name__ == "__main__":
    app.run(debug=True)
