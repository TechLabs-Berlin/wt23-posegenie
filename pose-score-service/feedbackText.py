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


def textGeneratorCurl(val_amp, val_minmax, val_time):
    if abs(val_amp) > 30:
        txtAngleComment = ' Excellent! Your exercise has a harmonic rhythm, which resulted in a good fitting.'
        txtAngleFeedback = 'Great job on your form! Make sure to focus on your biceps and not let your shoulders do the work.'
    elif 20 <= abs(val_amp) <= 30:
        txtAngleComment = ' Great! Your exercise has a harmonic rhythm. One or two things can be improved.'
        txtAngleFeedback = 'Good form was detected in the metrics. Try to focus on squeezing your biceps at the top of the curl.'
    elif 10 <= abs(val_amp) < 20:
        txtAngleComment = ' Good! A rhythm was detected in the red curve. One or two things can be improved.'
        txtAngleFeedback = 'Your form is decent. Try to focus on squeezing your biceps at the top of the curl.'
    elif abs(val_amp) < 10:
        txtAngleComment = ' No harmonicity detected.'
        txtAngleFeedback = 'Something looks off. Make sure you are performing a biceps curl exercise and not something else.'
    else:
        txtAngleComment = ' '
        txtAngleFeedback = ' '
    if abs(val_minmax) > 50:
        txtMinMaxComment = 'Huge range of motion!'
        txtMinMaxFeedback = 'You may want to decrease the range of motion and focus on proper form instead.'
    elif 10 < abs(val_minmax) <= 50:
        txtMinMaxComment = ' Looks like your range of motion is on point.'
        txtMinMaxFeedback = ' '
    elif abs(val_minmax) <= 10:
        txtMinMaxComment = ' Your range of motion is rather limited.'
        txtMinMaxFeedback = 'Make sure to go through a full range of motion while keeping good form.'

    if abs(val_time) < 1.0:
        txtTimeComment = ' No need to rush! An optimal time period per rep would be 1-3 seconds.'
        txtTimeFeedback = 'Try to slow down your movements and focus on squeezing your biceps at the top of the curl to increase muscle activation!'
    elif 1.0 <= abs(val_time) < 3.0:
        txtTimeComment = ' Great timing per rep!'
        txtTimeFeedback = 'Good job on your timing! Try to focus on squeezing your biceps at the top of the curl to increase muscle activation!'
    elif abs(val_time) > 3.0:
        txtTimeComment = ' Your reps are a bit slow.'
        txtTimeFeedback = 'Try to increase the speed of your reps while maintaining good form to add a bit of challenge!'

    txtMaxMin = 'The maximum - minimum angle reached throughout the exercise is ' + str(val_minmax) + '.'
    txtFitting = 'Your harmonic angle progression throughout the exercise is ' + str(abs(val_amp)) + '.'
    txtTime = 'The time spent on one rep:' + str(val_time)

    txt1 = r"$\bf{" + 'Definition:' + "}$" + '\nHere is a recording of your elbow angle. When you perform a biceps curl exercise, your elbow joint moves in a rhythmic pattern. This harmonic up and down motion of your elbow over time can be mapped onto the curve of a sine wave. By analyzing the angle of your elbow joint throughout the workout and fitting a sine wave to that data, we can see how consistent your movements are and how well you are maintaining the correct form. This information can help you improve your technique and get the most out of your workouts.'
    txt2 =  r"$\bf{" + 'Analysis:' + "}$" + '\nHere I fit your recording to a sine wave. This is an estimation for your workout.\n' + txtMaxMin + txtMinMaxComment + txtFitting + txtAngleComment + txtTime + txtTimeComment
    txt3 = r"$\bf{" + 'Feedback:' + "}$" + "\n"+  txtMinMaxFeedback + txtAngleFeedback + txtTimeFeedback
    return txt1, txt2, txt3

def textGeneratorSquat(val_amp, val_minmax, val_time):
    if abs(val_amp) > 70:
        txtAngleComment = ' Great result! Your exercise has a harmonic rhythm, which resulted in a good fitting.'
        txtAngleFeedback = 'A great form was detected in the metrics. Make sure to feel the exercise in your quads and glutes, and not in your lower back. Remember to engage your core!'
    elif 30 <= abs(val_amp) < 70:
        txtAngleComment = ' Great result! Your exercise has a harmonic rhythm. One or two things can be improved.'
        txtAngleFeedback =  'A good form was detected in the metrics. You may want to focus on your flexibility and increasing range of motion. Have you properly warmed up? Make sure to feel the exercise in your quads and glutes, and not in your lower back. Remember to engage your core!'
    elif 15 <= abs(val_amp) < 30:
        txtAngleComment = ' Good result! A rhythm was detected in the red curve. One or two things can be improved.'
        txtAngleFeedback = 'You may want to focus on your flexibility and increasing range of motion. Have you properly warmed up? Make sure to feel the exercise in your quads and glutes, and not in your lower back. Remember to engage your core!'
    elif abs(val_amp) < 15:
        txtAngleComment = ' No harmonicity detected.'
        txtAngleFeedback = ' Something looks fishy. Is this a squat video?! Please check the general guidelines and suggestions first.'
    else:
        txtAngleComment = ' '
        txtAngleFeedback = ' '

    if abs(val_minmax) > 130:
        txtMinMaxComment = 'Huge range of motion!'
        txtMinMaxFeedback = 'This is a big range of motion, why?'
    elif 40 < abs(val_minmax) <= 130:
        txtMinMaxComment = ' '
        txtMinMaxFeedback = ' '
    elif abs(val_minmax) <= 40:
        txtMinMaxComment = ' Your range of motion is rather limited.'
        txtMinMaxFeedback = ' Something looks fishy. Is this a squat video?! Please check the general guidelines and suggestions first.'

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

    txt1 = r"$\bf{" + 'Definition:' + "}$" + '\nHere is a recording of your hip-knee angle. When you perform a squat exercise, your hip and knee joints move in a rhythmic pattern. When you perform a lunge exercise, your hip and knee joints move in a rhythmic pattern. This harmonic up and down motion of your joints over time can be mapped onto the curve of a sine wave. By analyzing the angle of your hip and knee joints throughout the workout and fitting a sine wave to that data, we can see how consistent your movements are and how well you are maintaining the correct form. This information can help you improve your technique and get the most out of your workouts.'
    txt2 =  r"$\bf{" + 'Analysis:' + "}$" + '\nHere I fit your recording to a sine wave. This is an estimation for your workout.\n' + txtMaxMin + txtMinMaxComment + txtFitting + txtAngleComment + txtTime + txtTimeComment
    txt3 = r"$\bf{" + 'Feedback:' + "}$" + "\n"+  txtMinMaxFeedback + txtAngleFeedback + txtTimeFeedback
    return txt1, txt2, txt3
