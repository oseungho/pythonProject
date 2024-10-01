document.addEventListener('DOMContentLoaded', function(){ // DOMContentLoaded는 페이지의 DOM이 완전히 로드된 후에 실행
    document.getElementById('searchForm').addEventListener('submit', function(event){ // submit 이벤트는 폼이 제출될 때 발생
        console.log("클릭 이벤트 발생");
        event.preventDefault(); // 폼 기본 제출 동작 방지

        var searchText = document.getElementById('text-input').value; //입력된 텍스트 값 가져오기
        var searchType = document.getElementById('select-box').value; //선택한 타입 값 가져오기

        console.log('searchType : ', searchType, ' searchText : ', searchText);

        if(!searchText.trim()){
            alert('검색어를 입력해주세요.');
            return;
        }

        // 로딩 스피너 표시
        document.getElementById('loading').style.display = 'flex';

        // Axios를 사용하여 Flask API를 호출합니다.
        axios.get(`/youtube`, {
            params: {
                search: searchText,
                searchtype: searchType
            }
        })
        .then(response => {
            const results = response.data.result; // JSON 객체
            const searchtype = response.data.searchtype;
            console.log("전달받은 Data : ", results);
            const gridDiv = document.getElementById('grid-div');
            gridDiv.innerHTML = ''; // 기존 내용 제거

            // 객체의 각 프로퍼티를 순회
            for(const key in results){
                if(results.hasOwnProperty(key)){
                    const data = results[key]; //각 광고 항목을 가져옴

                    const adElement = document.createElement('div');
                    adElement.classList.add('grid-item');
                    if(searchtype == 1){

                        console.log(`Index: ${data.index}, Title: ${data.title}, Description: ${data.description}`);

                        adElement.innerHTML = `
                            <div class="grid-item-contents">
                                <h2>${data.title}</h2>
                                <p>${data.description}</p>
                            </div>
                        `;
                    }
                    else if(searchtype == 2){

                        console.log(`Index: ${data.index}, Title: ${data.title}, Description: ${data.description}`);

                        adElement.innerHTML = `
                            <div class="grid-item-contents">
                                <h2>${data.title}</h2>
                                <p>${data.href}</p>
                                <p>${data.image}</p>
                            </div>
                        `;
                    }
                    else{
                        console.log('하하하')
                    }
                    gridDiv.appendChild(adElement);
                }
            }
        })
        .catch(error => {
            console.error('오류 발생:', error);
        })
        .finally(()=>{
            // 로딩 스피너 숨기기
            document.getElementById('loading').style.display = 'none';
        })
    })
})

/*
 AJAX : 웹 페이지가 전체 페이지를 새로 고치지 않고도 서버와 비동기적으로 데이터를 주고 받을 수 있도록 해주는 기술
        (데이터를 비동기적으로 요청하고 처리 - 웹 페이지를 동적으로 업데이트)

        [AJAX 기술을 동작할 수 있게 해주는 주요 API]
        1. XMLHttpRequest -> JavaScript API
            - 오래된 API, 비동기 요청을 처리 가능
            - 문법이 복잡, 프로미스 미사용

        2. fetch -> XMLHttpRequest를 대체하기 위해 도입된 최신 API
            - 프로미스 기반의 간결한 문법 제공
            - JSON 변환과 에러 처리가 간단, 명확
            - 단, 일부 구형 브라우저에서 지원이 안될 수 있음

        3. Axios
            - 외부 라이브러리, fetch와 XMLHttpRequest의 기능을 확장하고 간편하게 사용하도록 설계
            - 요청 및 응답 인터셉터, 자동 JSON 변환, CSRF 보호 등의 추가 기능을 제공
            - 브라우저와 Node.js에서 모두 사용 가능 (프로미스 사용 o)

 * 정리
    - fetch, XMLHttpRequest는 브라우저 내장 API
    - Axios는 외부 라이브러리로 제공되는 도구

    프로미스란?
        - 자바스크립트의 비동기 작업을 다루기 위한 객체
        - 미래의 완료나 실패를 나타내는 값으로, 비동기 작업의 결과를 나중에 사용할 수 있게 해줌
*/