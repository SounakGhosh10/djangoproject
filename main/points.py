# In TaskViewSet or a custom admin endpoint:
@action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
def approve(self, request, pk=None):
    task = get_object_or_404(Task, pk=pk)
    task.status = "APPROVED"
    task.save()

    # add points to user
    user = task.user
    user.points += task.app.points
    user.save()

    return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
