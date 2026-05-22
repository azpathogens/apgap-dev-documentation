
class AccessRequestApproverSerializer(serializers.ModelSerializer):
    
    Serializer for AccessRequestApprover through model.
    



class AccessRequestListSerializer(serializers.ModelSerializer):
    
    Lightweight serializer for listing access requests.
    



class AccessRequestDetailSerializer(serializers.ModelSerializer):
    
    Detailed serializer for access request information.
    


    def get_approvers_list(self, obj):
        Get all approvers for this access request.
        Uses prefetched access_request_approvers to avoid N+1 queries.
        # Use prefetched data - .all() uses the prefetch cache
        approvers = obj.access_request_approvers.all()


class AccessRequestCreateUpdateSerializer(serializers.ModelSerializer):
    
    Serializer for creating and updating access requests.
    Approvers are automatically set to all lab directors of the file's lab.
    Status defaults to PENDING if not provided.
    


    def validate_status(self, value):
        
        Validate that the status is a valid choice.
        

    def validate_file(self, value):
        
        Validate that the file is not archived.
        Access cannot be requested for archived files since the underlying data no longer exists.
        

    def _get_lab_directors(self, file):
        
        Get all lab directors for the given file's lab.
        

    def create(self, validated_data):
        
        Create a new access request with approvers automatically set to lab directors.
        


    def update(self, instance, validated_data):
        
        Update an access request. If file changes, update approvers to new lab's directors.
        
