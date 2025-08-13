from django.urls import path,include
from .import views
from rest_framework.routers import DefaultRouter
from .views import TableViewSet, ReservationViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router=DefaultRouter()
router.register(r'tables',TableViewSet)
router.register(r'reservations',ReservationViewSet)

urlpatterns = [
    path('',views.login_view,name="login"),
    path('signup/',views.signup_view,name="signup"),
    # path('signup/login/',views.login_view,name='login'),
    path('home/',views.home,name="home"),
    path('reservation/',views.reservation,name="reservation"),
    path('cancel/<int:pk>/', views.cancel_reservation, name="cancel_reservation"),
    path('update/<int:pk>/', views.update_reservation, name="update_reservation"),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
