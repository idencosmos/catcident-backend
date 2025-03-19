# uploads/tasks.py
import logging
import requests
from celery import shared_task
from .utils import update_media_usage, clean_unused_media

logger = logging.getLogger(__name__)


@shared_task
def update_media_usage_async():
    """미디어 사용 여부를 비동기적으로 확인합니다."""
    try:
        updated_count = update_media_usage()
        logger.info(f"미디어 사용 여부 업데이트 완료: {updated_count}개 항목 업데이트")
        return {"status": "success", "updated_count": updated_count}
    except Exception as e:
        logger.error(f"미디어 사용 여부 업데이트 실패: {e}")
        return {"status": "error", "message": str(e)}


@shared_task
def clean_unused_media_async():
    """사용되지 않는 미디어 파일을 비동기적으로 정리합니다."""
    try:
        # 먼저 사용 여부 체크
        update_media_usage()
        # 미사용 파일 정리
        deleted_count = clean_unused_media()
        logger.info(f"미사용 미디어 정리 완료: {deleted_count}개 항목 삭제")
        return {"status": "success", "deleted_count": deleted_count}
    except Exception as e:
        logger.error(f"미사용 미디어 정리 실패: {e}")
        return {"status": "error", "message": str(e)}


@shared_task
def clean_unused_media_task():
    """
    주기적으로 실행될 미디어 정리 태스크
    Celery Beat에 의해 스케줄링 됨
    """
    return clean_unused_media_async()


@shared_task
def check_system_health():
    """시스템의 전반적인 상태를 확인하고 결과를 반환합니다."""
    try:
        # 내부 헬스체크 URL 호출 (Docker 내부망에서의 통신)
        response = requests.get("http://localhost:8000/healthcheck/", timeout=10)
        
        # 결과 상태 확인
        if response.status_code == 200:
            health_data = response.json()
            all_services_ok = all(service.get("status") == "working" for service in health_data)
            
            if all_services_ok:
                logger.info("모든 시스템 서비스가 정상적으로 작동 중입니다.")
                return {"status": "healthy", "details": health_data}
            else:
                # 문제가 있는 서비스 식별
                failing_services = [
                    service.get("service") for service in health_data 
                    if service.get("status") != "working"
                ]
                logger.warning(f"일부 서비스에 문제가 있습니다: {failing_services}")
                return {"status": "degraded", "failing_services": failing_services, "details": health_data}
        else:
            logger.error(f"헬스체크 요청이 실패했습니다. 상태 코드: {response.status_code}")
            return {"status": "error", "message": f"헬스체크 요청 실패 (HTTP {response.status_code})"}
    
    except requests.exceptions.Timeout:
        logger.error("헬스체크 요청이 시간 초과되었습니다.")
        return {"status": "error", "message": "헬스체크 요청 시간 초과"}
    
    except requests.exceptions.ConnectionError:
        logger.error("헬스체크 서비스에 연결할 수 없습니다.")
        return {"status": "error", "message": "헬스체크 서비스 연결 실패"}
    
    except Exception as e:
        logger.error(f"헬스체크 과정에서 예상치 못한 오류가 발생했습니다: {e}")
        return {"status": "error", "message": str(e)}
