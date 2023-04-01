def textGenerator(val_amp, val_minmax, val_time):
	if abs(val_amp) > 55:
		txtAngleComment = ' Great result! Your exercise has a harmonic rhythm, which resulted in a good fitting.'
		txtAngleFeedback = 'A great form was detected in the metrics. Make sure to feel the exercise in your quads and hamstrings, and not in your lower back.'
	elif 20 <= abs(val_amp) < 55:
		txtAngleComment = ' Great result! Your exercise has a harmonic rhythm. One or two things can be improved.'
		txtAngleFeedback =  'A good form was detected in the metrics. You may want to focus on your flexibility and increasing range of motion. Have you properly warmed up? Make sure to feel the exercise in your quads and hamstrings, and not in your lower back.'
	elif 10 <= abs(val_amp) < 20:
		txtAngleComment = ' Good result! A rhythm was detected in the red curve. One or two things can be improved.'
		txtAngleFeedback = 'You may want to focus on your flexibility and increasing range of motion. Have you properly warmed up? Make sure to feel the exercise in your quads and hamstrings, and not in your lower back.'
	elif abs(val_amp) < 10:
		txtAngleComment = ' No harmonicity detected.'
		txtAngleFeedback = ' Something looks fishy. Is this a lunge video?! Please check the general guidelines and suggestions first.'
	else:
		txtAngleComment = ' '
		txtAngleFeedback = ' '

	if abs(val_minmax) >120:
		txtMinMaxComment = 'Huge range of motion!'
		txtMinMaxFeedback = 'This is a big range of motion, why?'
	elif 25 < abs(val_minmax) <= 120:
		txtMinMaxComment = ' '
		txtMinMaxFeedback = ' '
	elif abs(val_minmax) <= 25:
		txtMinMaxComment = ' Your range of motion is rather limited.'
		txtMinMaxFeedback = ' Something looks fishy. Is this a lunge video?! Please check the general guidelines and suggestions first.'

	if abs(val_time) < 1.0:
		txtTimeComment = ' No need to rush! An optimal time period per rep would be 1-3 seconds.'
		txtTimeFeedback = ' Try to spend more time in one rep. This will increase your endurance!'
	elif 1.0 <= abs(val_time) < 3.0:
		txtTimeComment = ' Great timing per rep!'
		txtTimeFeedback = ' You can increase your time per rep to increase your endurance, or use weights to add challenge!'
	elif abs(val_time) > 3.0:
		txtTimeComment = ' You stay a bit long during each rep.'
		txtTimeFeedback = ' As long as there is no pain, it is OK to have long reps.'
	txtMaxMin  = 'The maximum - minimum angle reached throughout the exercise is ' + str(val_minmax) + '.'
	txtFitting = 'Your harmonic angle progression throughout the exercise is ' + str(abs(val_amp)) + '.'
	txtTime = 'The time spent on one rep:' + str(val_time)

	txt1 = r"$\bf{" + 'Definition:' + "}$" + '\nHere is a recording of your hip-knee angle. When you perform a lunge exercise, your hip and knee joints move in a rhythmic pattern. This harmonic up and down motion of your joints over time can be mapped onto the curve of a sine wave. By analyzing the angle of your hip and knee joints throughout the workout and fitting a sine wave to that data, we can see how consistent your movements are and how well you are maintaining the correct form. This information can help you improve your technique and get the most out of your workouts.'
	txt2 =  r"$\bf{" + 'Analysis:' + "}$" + '\nHere I fit your recording to a sine wave. This is an estimation for your workout.\n' + txtMaxMin + txtMinMaxComment + txtFitting + txtAngleComment + txtTime + txtTimeComment
	txt3 = r"$\bf{" + 'Feedback:' + "}$" + "\n"+  txtMinMaxFeedback + txtAngleFeedback + txtTimeFeedback
	return txt1, txt2, txt3
