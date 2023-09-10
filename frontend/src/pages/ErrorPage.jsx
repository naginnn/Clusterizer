import {PageWrapper} from "../components/PageWrapper";
import {ErrorModal} from "../components/ErrorModal";

export const ErrorPage = ({error = {}}) => {
    return (
        <PageWrapper>
            <ErrorModal error={error}/>
        </PageWrapper>
    )
}