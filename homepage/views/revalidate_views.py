"""
/homepage/views/revalidate_views.py
Next.js 캐시 태그를 재검증하기 위한 API 엔드포인트 정의
프론트엔드에서 백엔드 콘텐츠 변경사항을 반영하기 위한 온디맨드 재검증 메커니즘 제공
"""

import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from ..signals import revalidate_all_nextjs_tags, ALL_TAGS

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def revalidate_cache(request):
    """
    Next.js 캐시 태그 재검증 API 엔드포인트
    프론트엔드 배포 후 모든 태그를 한 번에 재검증합니다.
    """
    # 보안: 인증 토큰 검증
    auth_header = request.headers.get("Authorization", "")
    if (
        not auth_header.startswith("Bearer ")
        or auth_header[7:] != settings.NEXTJS_REVALIDATE_TOKEN
    ):
        logger.warning("재검증 API 인증 실패 시도 감지")
        return JsonResponse({"error": "인증 실패"}, status=401)

    try:
        data = json.loads(request.body)
        action = data.get("action")

        if action == "revalidate_all_tags":
            tag_count = revalidate_all_nextjs_tags()

            logger.info(f"API 요청으로 {tag_count}개 태그 재검증 완료")
            return JsonResponse(
                {
                    "success": True,
                    "message": f"총 {tag_count}개 태그 재검증 완료",
                    "revalidated_tags": ALL_TAGS,
                }
            )
        else:
            logger.warning(f"알 수 없는 액션 요청: {action}")
            return JsonResponse({"error": "알 수 없는 액션"}, status=400)

    except Exception as e:
        logger.error(f"캐시 재검증 중 오류 발생: {e}")
        return JsonResponse({"error": str(e)}, status=500)
