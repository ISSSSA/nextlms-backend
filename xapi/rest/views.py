
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from ..serializers import XAPIStatementSerializer
from ..models import XAPIStatement


class XAPIStatementView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data

        if 'statements' in data:
            statements = data['statements']
            results = []
            for statement in statements:
                serializer = XAPIStatementSerializer(data=statement)
                if serializer.is_valid():
                    serializer.save()
                    results.append({"success": True, "statement_id": serializer.data['statement_id']})
                else:
                    results.append({"success": False, "errors": serializer.errors})

            return Response(results, status=status.HTTP_207_MULTI_STATUS)
        else:
            serializer = XAPIStatementSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True, "statement_id": serializer.data['statement_id']},
                                status=status.HTTP_201_CREATED)
            return Response({"success": False, "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class XAPIStatementGetView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, statement_id, format=None):
        try:
            statement = XAPIStatement.objects.get(statement_id=statement_id)
            serializer = XAPIStatementSerializer(statement)
            return Response(serializer.data)
        except XAPIStatement.DoesNotExist:
            return Response({"success": False, "error": "Statement not found"},
                            status=status.HTTP_404_NOT_FOUND)