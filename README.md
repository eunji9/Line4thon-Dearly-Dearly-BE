# Line4thon-Dearly-Dearly-BE
<h1>
  추후 업데이트 예정입니다.
</h1>

<h2>
  **🌿 Git 브랜치 전략**

  본 프로젝트는 **GitHub Flow**를 기반으로 하되, 협업에 맞게 브랜치 전략을 다음과 같이 정의합니다:

  - `main` : 배포용 브랜치 (항상 안정적인 버전 유지)
  - `dev` : 개발 통합 브랜치 (기능 개발 완료 후 PR 머지 대상)
  - `feat-기능명` : 개별 기능 개발 브랜치예시) `feat-login`, `feat-pdf-parser`

  **💡 Workflow**

  1. 기능 선택
  2. 브랜치 생성: `feat-기능명`
  3. 기능 개발 후 `dev` 브랜치로 Pull Request 생성
  4. 본인 제외하고 다른 사람이 머지
  5. `main` 브랜치는 일정 단위로 `dev`에서 안정화된 버전만 머지
</h2>