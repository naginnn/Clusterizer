export const normalizeData = (data) => {
    const allQuestion = {}

    data.forEach(answer => {
        if (answer.question_id in allQuestion) {
            allQuestion[answer.question_id].answers.push({
                answer: answer.answer,
                cluster: answer.cluster,
                context_cluster: answer.context_cluster,
                corrected: answer.corrected,
                count: answer.count,
                sentiment: answer.sentiment
            })
            return
        }

        allQuestion[answer.question_id] = {
            answers: [{
                answer: answer.answer,
                cluster: answer.cluster,
                context_cluster: answer.context_cluster,
                corrected: answer.corrected,
                count: answer.count,
                sentiment: answer.sentiment
            }],
            question: answer.question
        }
    })

    return Object.values(allQuestion)
}