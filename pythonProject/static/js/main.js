// 전역에서 showTab 함수 정의
function showTab(tabName) {
    // 모든 탭 콘텐츠 숨기기
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // 선택한 탭 콘텐츠 보이기
    const selectedTab = document.getElementById(tabName);
    selectedTab.classList.add('active');

    // # grid-div 보이기 (youtube 탭인 경우)
    const gridDiv = document.getElementById('grid-div');
    if (tabName === 'youtube') {
        gridDiv.style.display = 'block'; // 유튜브 탭이 선택된 경우 grid-div를 보이게 함
    } else {
        gridDiv.style.display = 'none'; // 다른 탭이 선택된 경우 grid-div를 숨김
    }

    // # bs4_Results 보이기 (naver_bs4 탭인 경우)
    const bs4Div = document.getElementById('bs4_Results');
    if (tabName === 'naver_bs4') {
        bs4Div.style.display = 'block'; // naver_bs4 탭이 선택된 경우, 보이게 함
    } else {
        bs4Div.style.display = 'none'; // 다른 탭이 선택된 경우 naver_bs4를 숨김
    }

    // # naverResults 보이기 (naver 탭인 경우)
    const naverDiv = document.getElementById('naverResults');
    if (tabName === 'naver') {
        naverDiv.style.display = 'block'; // naver_bs4 탭이 선택된 경우, 보이게 함
    } else {
        naverDiv.style.display = 'none'; // 다른 탭이 선택된 경우 naver를 숨김
    }

    // 현재 활성화된 버튼 상태 변경
    const tabButtons = document.querySelectorAll('.tab');
    tabButtons.forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`.tab[onclick="showTab('${tabName}')"]`).classList.add('active');
}

document.addEventListener('DOMContentLoaded', function() {
    // 검색 폼 제출 이벤트 핸들러
    document.querySelector('.searchForm').addEventListener('submit', function(event) {
        event.preventDefault(); // 폼 기본 제출 동작 방지
        console.log("클릭 이벤트 발생");

        // 로딩 스피너 동작
        const loadingSpinner = document.getElementById('loadingSpinner');
        loadingSpinner.style.display = 'block'; // 로딩 스피너 보이기

        // 현재 활성화된 탭 확인
        const activeTab = document.querySelector('.tab-content.active');
        const searchType = activeTab.querySelector('.select-box').value; // 선택한 타입 값 가져오기

        console.log('searchType : ', searchType);
            // 네이버 탭인 경우
            if (activeTab.id === 'naver') {
                // 크롤링 시작하기 전에 숫자값을 전달받았는지 유효성 검사
                const input_value = activeTab.querySelector('.text-input').value;

                // 검색어가 비어 있는지 검사
                if (!input_value.trim()) {
                    alert('검색어를 입력해주세요.');
                    loadingSpinner.style.display = 'none'; // 로딩 스피너 숨기기
                    return;
                }

                // 숫자가 아닌 입력을 검사
                if (!/^\d+$/.test(input_value)) {  // 숫자만 허용
                    alert('숫자만 입력해주세요.');
                    loadingSpinner.style.display = 'none'; // 로딩 스피너 숨기기
                    return;
                }
                // 검색 타입만 사용
                const searchText = activeTab.querySelector('.text-input').value; // 입력된 텍스트 값 가져오기
                collectNaverNews(searchType, searchText, 1);
            } else if(activeTab.id === 'naver_bs4'){

                collectNaverNews(searchType, 0, 2);
            }else {
            // 유튜브 검색 로직
            const searchText = activeTab.querySelector('.text-input').value; // 입력된 텍스트 값 가져오기

            console.log('searchText : ', searchText);

            if (!searchText.trim()) {
                alert('검색어를 입력해주세요.');
                return;
            }

            axios.get(`/youtube`, {
                params: {
                    search: searchText,
                    searchtype: searchType
                }
            })
            .then(response => {
                const results = response.data.result; // JSON 객체
                const gridDiv = document.getElementById('grid-div');
                gridDiv.innerHTML = ''; // 기존 내용 제거

                // 객체의 각 프로퍼티를 순회
                for (const key in results) {
                    if (results.hasOwnProperty(key)) {
                        const data = results[key]; // 각 광고 항목을 가져옴
                        const adElement = document.createElement('div');
                        adElement.classList.add('grid-item');
                        adElement.innerHTML = `
                            <div class="grid-item-contents">
                                <a href=${data.href}><h2>${data.title}</h2></a>
                                <p>${data.description}</p>
                                <img src=${data.image}></img>
                            </div>
                        `;
                        gridDiv.appendChild(adElement);
                    }
                }
            })
            .catch(error => {
                console.error('오류 발생:', error);
            })
            .finally(() => {
                loadingSpinner.style.display = 'none'; // 로딩 스피너 숨기기
            });
        }
    });

    // 숫자만 입력될 수 있도록 실시간 필터링
//    document.getElementById('naverInput').addEventListener('input', function() {
//        this.value = this.value.replace(/[^0-9]/g, ''); // 숫자 이외의 문자 제거
//    });

    function collectNaverNews(searchType, searchText, tab_type) {
        let url = '';

        // 조건에 맞게 URL 선택
        if (tab_type == 1) {
            url = `http://127.0.0.1:5000/news?searchtype=${searchType}&searchText=${searchText}`;
        } else {
            url = `http://127.0.0.1:5000/news_bs4?searchtype=${searchType}`;
        }

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data); // 데이터 구조 확인
//                const naverArticles = document.querySelector('#naver-articles');
                // ID 동적 설정
                const naverArticles = document.querySelector(`#naver-articles${tab_type === 1 ? '' : '_bs4'}`); // tab_type에 따라 ID 설정
                naverArticles.innerHTML = ''; // 기존 내용 제거

                // 데이터가 배열인지 확인
                if (!Array.isArray(data)) {
                    console.error('Expected data to be an array:', data);
                    return;
                }

                data.forEach(item => {
                    // item의 구조가 올바른지 확인
                    if (!item.title || !item.link || !item.imageUrl || !item.summary || !item.company || !item.date) {
                        console.error('Invalid item structure:', item);
                        return; // 잘못된 구조면 넘어감
                    }

                    // 카드 생성
                    const card = document.createElement('div');
                    card.setAttribute('class', "card col-sm-4"); // 너비 조절

                    // 링크 생성
                    const a = document.createElement('a');
                    a.setAttribute('href', item.link);
                    a.target = "_blank"; // 새 탭에서 열기
                    a.style.textDecoration = 'none'; // 링크 스타일 제거

                    // 이미지 추가
                    const img = document.createElement('img');
                    img.className = 'card-img-top';
                    // URL 수정하여 고화질 이미지 요청
                    // imageUrl이 유효한지 확인한 후 URL 수정
                    if (item.imageUrl) {
                        const highQualityImageUrl = item.imageUrl.replace(/type=\w+\d+_\d+/, 'type=ofullfill1068_720');
                        img.src = highQualityImageUrl; // 이미지 주소
                    } else {
                        img.src = 'default_image_url.jpg'; // 기본 이미지 URL (없을 경우)
                    }
                    img.alt = item.title; // 접근성을 위한 alt 속성

                    // 카드 본문
                    const cardBody = document.createElement('div');
                    cardBody.setAttribute('class', "card-body");

                    // 제목
                    const h4 = document.createElement('h4');
                    h4.setAttribute('class', "card-title");
                    h4.textContent = item.title; // 제목

                    // 요약
                    const p = document.createElement('p');
                    p.setAttribute('class', "card-text");
                    p.textContent = item.summary; // 요약

                    // 신문사
                    const companySpan = document.createElement('span');
                    companySpan.setAttribute('class', 'company-name')
                    companySpan.textContent = item.company;

                    // 날짜
                    const dateSpan = document.createElement('span');
                    dateSpan.setAttribute('class', 'date');
                    dateSpan.textContent = item.date; // 날짜

                    // 신문사와 날짜를 같은 줄에 배치
                    const companyAndDateContainer = document.createElement('div');
                    companyAndDateContainer.setAttribute('class', 'company-and-date');
                    companyAndDateContainer.appendChild(dateSpan);
                    companyAndDateContainer.appendChild(companySpan);

                    // 요소들 결합
                    cardBody.appendChild(h4);
                    cardBody.appendChild(p);
                    cardBody.appendChild(companyAndDateContainer); // 신문사와 날짜를 포함한 컨테이너
                    a.appendChild(img);
                    card.appendChild(a);
                    card.appendChild(cardBody);
                    naverArticles.appendChild(card);
                });
                naverArticles.style.display = 'flex';
                naverArticles.style.flexWrap = 'wrap'; // 카드가 잘 보이도록 줄바꿈 설정
            })
            .catch(error => {
                console.error('오류 발생:', error);
            })
            .finally(() => {
                loadingSpinner.style.display = 'none'; // 로딩 스피너 숨기기
            });
    }

    // 탭 클릭 이벤트 등록
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function() {
            const tabName = this.getAttribute('onclick').match(/'([^']+)'/)[1];
            showTab(tabName);
        });
    });
});



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