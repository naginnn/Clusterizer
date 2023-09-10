import {useCallback, useState} from "react";

export const usePagination = () => {
    const [rowsPerPage, setRowsPerPage] = useState(10)
    const [page, setPage] = useState(0)

    const onChangePage = useCallback((event, newPage) => {
        setPage(newPage);
    }, [rowsPerPage])

    const сhangeRowsPerPage = useCallback((event) => {
        setPage(0);
        setRowsPerPage(+event.target.value);
    }, [])

// Проверка есть ли контект на текущей странице, если контента нет
// переключает на первую страницу, такое возможно когда данные динамически изменяются
    const getActualPage = (content) => {
        if (Math.trunc(content.length / rowsPerPage) < page) {
            onChangePage(undefined, 0)
            return 0
        }

        return page
    }

    const getPageContent = useCallback((content) => {
        const actualPage = getActualPage(content)

        return content.slice(actualPage * rowsPerPage, actualPage * rowsPerPage + rowsPerPage);
    }, [rowsPerPage, page])

// Если данных стало меньше и такой страницы существовать не может, то
// переключится на 1 страницу
    const getPage = useCallback((content) => {
        const actualPage = getActualPage(content)

        return actualPage
    }, [rowsPerPage, page])

    return {onChangePage, getPageContent, rowsPerPage, сhangeRowsPerPage, getPage};
}
