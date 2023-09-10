import {useMemo, useState, useEffect} from "react";

import {Treemap, Tooltip} from "recharts"

import {Typography, Paper, Box, TablePagination} from "@mui/material"

import {exampleData} from './exampleData'
import {ResponsiveContainer} from "recharts";
import {usePagination} from "../../hooks/usePagination";

export const emotionColors = {
    negatives: 'red',
    positives: 'green',
    neutrals: 'orange',
    withoutEmotion: 'blue'
}

const emotionColorsRus = {
    'red': 'Негативный',
    'green': 'Положительный',
    'orange': 'Нейтральный',
    'withoutEmotion': 'Нет данных',
    'negatives': 'Негативный',
    'positives': 'Положительный',
    'neutrals': 'Нейтральный',
}

//Обязательно так должны называться поля
const addSizeAndEmotionalColor = (data) => {
    return data.map(question => {
        const emotionalColorCount = {
            negatives: 0,
            positives: 0,
            neutrals: 0
        }

        let size = 0

        question.answers.forEach(answer => {
            if (answer.sentiment) {
                emotionalColorCount[answer.sentiment] += answer.count
            }
            if (answer.count) {
                size += answer.count
            }
        })

        if (!emotionalColorCount.neutrals && !emotionalColorCount.positives && !emotionalColorCount.negatives) {
            return {
                emotionalColor: emotionColors.withoutEmotion,
                size,
                ...question
            }
        }

        const sumColor = Object.entries(emotionalColorCount).reduce((accum, curr) => {
            return accum[1] > curr[1] ? accum : curr
        })

        return {
            emotionalColor: emotionColors[sumColor[0]] || emotionColors.withoutEmotion,
            size,
            ...question
        }
    })
}

export const TreeMapQuestionChart = ({data = exampleData, dataKey = 'size'}) => {
    const [subTree, setSubTree] = useState(null)
    const {onChangePage, getPageContent, rowsPerPage, сhangeRowsPerPage, getPage} = usePagination()

    const dataWithEmotionColors = useMemo(() => {
        return addSizeAndEmotionalColor(data)
    }, [])

    useEffect(() => {
        onChangePage(null, 0)
        сhangeRowsPerPage({target: {value: 0}})
    }, [subTree])

    const CustomizedQuestionContent = (props) => {
        const {root, depth, x, y, width, height, index, question, emotionalColor, size} = props;
        const fixTextWidth = 200
        const fixTextHeight = 50

        const getQuestion = () => {
            if (width >= 200 && width <= 250) {
                return question.length > 25
                    ? question.slice(0, 25).trim() + '...'
                    : question
            } else if (width > 250 && width <= 280) {
                return question.length > 30
                    ? question.slice(0, 30).trim() + '...'
                    : question
            } else if (width > 280 && width <= 300) {
                return question.length > 35
                    ? question.slice(0, 35).trim() + '...'
                    : question
            } else if (width > 300) {
                return question.length > 40
                    ? question.slice(0, 40).trim() + '...'
                    : question
            }
            return ''
        }

        return (
            <g onClick={() => setSubTree(dataWithEmotionColors[index])}>
                <rect
                    x={x}
                    y={y}
                    width={width}
                    height={height}
                    style={{
                        fill: emotionalColor,
                        stroke: "#fff",
                        strokeWidth: 2 / (depth + 1e-10),
                        strokeOpacity: 1 / (depth + 1e-10)
                    }}
                />
                {depth === 1 && width >= fixTextWidth && height >= fixTextHeight ? (
                    <text
                        x={x + width / 2}
                        y={y + height / 2 + 7}
                        textAnchor="middle"
                        fill="#fff"
                        fontSize={14}
                    >
                        {
                            getQuestion()
                        }
                    </text>
                ) : null}
                {depth === 1 ? (
                    <text x={x + 4} y={y + 18} fill="#fff" fontSize={16} fillOpacity={0.9}>
                        {size + 1}
                    </text>
                ) : null}
            </g>
        );
    };

    const CustomizedAnswerContent = (props) => {
        const {root, depth, x, y, width, height, answer, sentiment, count, corrected} = props;
        const fixTextWidth = 90
        const fixTextHeight = 50

        const getAnswer = (answer) => {
            if (width >= 100 && width < 130) {
                return answer.length > 10
                    ? answer.slice(0, 10).trim() + '...'
                    : answer
            } else if (width >= 130 && width < 150) {
                return answer.length > 15
                    ? answer.slice(0, 15).trim() + '...'
                    : answer
            } else if (width >= 150 && width < 200) {
                return answer.length > 20
                    ? answer.slice(0, 20).trim() + '...'
                    : answer
            } else if (width >= 200 && width <= 250) {
                return answer.length > 25
                    ? answer.slice(0, 25).trim() + '...'
                    : answer
            } else if (width > 250 && width <= 280) {
                return answer.length > 30
                    ? answer.slice(0, 30).trim() + '...'
                    : answer
            } else if (width > 280 && width <= 300) {
                return answer.length > 35
                    ? answer.slice(0, 35).trim() + '...'
                    : answer
            } else if (width > 300) {
                return answer.length > 40
                    ? answer.slice(0, 40).trim() + '...'
                    : answer
            }
            return ''
        }

        return (
            <g onClick={() => setSubTree(null)}>
                <rect
                    x={x}
                    y={y}
                    width={width}
                    height={height}
                    style={{
                        fill: emotionColors[sentiment] || emotionColors.withoutEmotion,
                        stroke: "#fff",
                        strokeWidth: 2 / (depth + 1e-10),
                        strokeOpacity: 1 / (depth + 1e-10)
                    }}
                />
                {depth === 1 && width >= fixTextWidth && height >= fixTextHeight ? (
                    <text
                        x={x + width / 2}
                        y={y + height / 2 + 7}
                        textAnchor="middle"
                        fill="#fff"
                        fontSize={14}
                    >
                        {
                            getAnswer(corrected || answer)
                        }
                    </text>
                ) : null}
                {depth === 1 ? (
                    <text x={x + 4} y={y + 18} fill="#fff" fontSize={16} fillOpacity={0.9}>
                        {count + 1}
                    </text>
                ) : null}
            </g>
        );
    };

    const CustomQuestionTooltip = ({active, payload, label}) => {
        if (active && payload && payload.length) {
            return (
                <Paper sx={{p: '10px'}}>
                    <Typography>{`Вопрос: "${payload[0].payload.question}"`}</Typography>
                    <Typography>{`Количество ответов: ${payload[0].payload.size}`}</Typography>
                    <Typography>{`Эмоциональный окрас: ${emotionColorsRus[payload[0].payload.emotionalColor] || emotionColorsRus.withoutEmotion}`}</Typography>
                </Paper>
            );
        }

        return null;
    };

    const CustomAnswerTooltip = ({active, payload, label}) => {
        if (active && payload && payload.length) {
            return (
                <Paper sx={{p: '10px'}}>
                    <Typography>{`${payload[0].payload.corrected ? 'Оригинальный ответ: ' : 'Ответ: '}${payload[0].payload.answer}`}</Typography>
                    {
                        payload[0].payload.corrected &&
                        <Typography>{`Исправленный ответ: ${payload[0].payload.corrected}`}</Typography>
                    }
                    <Typography>{`Количество ответов : ${payload[0].payload.count}`}</Typography>
                    <Typography>{`Эмоциональный окрас : ${emotionColorsRus[payload[0].payload.sentiment] || emotionColorsRus.withoutEmotion}`}</Typography>
                </Paper>
            );
        }

        return null;
    };

    return (
        <Box>
            <ResponsiveContainer>
                {
                    !subTree
                        ? <Treemap
                            width='100%'
                            height='100%'
                            data={getPageContent(dataWithEmotionColors)}
                            dataKey={dataKey}
                            stroke="#fff"
                            fill="#8884d8"
                            animationDuration={700}
                            content={<CustomizedQuestionContent/>}
                        >
                            <Tooltip content={<CustomQuestionTooltip/>}/>
                        </Treemap>
                        : <Treemap
                            width='100%'
                            height='100%'
                            data={getPageContent(subTree.answers)}
                            dataKey={'count'}
                            stroke="#fff"
                            fill="#8884d8"
                            animationDuration={700}
                            content={<CustomizedAnswerContent/>}
                        >
                            <Tooltip content={<CustomAnswerTooltip/>}/>
                        </Treemap>
                }
            </ResponsiveContainer>
            <TablePagination
                rowsPerPageOptions={[10, 15, 20, 25, 50, 100, 150]}
                component="div"
                count={subTree ? subTree.length : data.length}
                rowsPerPage={rowsPerPage}
                page={getPage(subTree ? subTree : data)}
                onPageChange={onChangePage}
                onRowsPerPageChange={сhangeRowsPerPage}
                labelRowsPerPage={`Количество ${subTree ? 'ответов' : 'вопросов'} на странице`}
            />
        </Box>
    )
}