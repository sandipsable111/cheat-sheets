# !bin/bash
echo
echo
echo
echo "####################################################################################"
echo "#                                                                                  #"
echo "#        !!  WELCOME TO THE ANSIBLE VAULT SECRET UPDATION UTILITY  !!              #"
echo "#                                                                                  #"
echo "####################################################################################"
echo "                                                                                     "
echo " Using this utility you can : "
echo " 		- Add new secret key value pair in to APIs vault configuration file."
echo " 		- Update values of the existing keys from APIs vault configuration file."
echo "		- Do it for any targeted group of hosts/ remote servers / environment. "
echo
echo " Just by answering to the following quetions. "
echo " ____________________________________________________________________________________ "

#Variable declaration and initialization
secret_storage_path="/opt/sandip/"
secret_storage_file_name="/vault.yml"


echo
read -p 'Please Enter Targeted Host Group Name For Which You Want To Update API Secrets : ' host_group_name

if [ -d $secret_storage_path$host_group_name ]; then
   echo
   echo " What action do you want to perform:              "
   echo "1. Add new secret key value pair.          "
   echo "2. Update value of the existing secret key."
   echo
   read -p  "Enter your choice (1/2): " user_choice
   echo 

   ansible-vault decrypt $secret_storage_path$host_group_name$secret_storage_file_name &>> utility_log.txt

   case $user_choice in
        1)
                echo "You have choosen: 1. Add new secret key value pair."                
                #add_key_value $host_group_name ; 
		echo		
				
		echo "Any newly added key value pair will  be appended at the end of the file."
		echo
		read -p 'Enter new secret key: ' secret_key_name
		echo
		read -s -p 'Enter key value: ' secret_key_value
		echo
		read -s -p "Confirm key value : "  confirm_secret_key_value
		echo

		   if [[ "$secret_key_value" == "$confirm_secret_key_value" ]]; then
			   echo $secret_key_name": \""$confirm_secret_key_value "\"" >>  $secret_storage_path$host_group_name$secret_storage_file_name
			   echo "                                                                                      "
			   echo " Success !!  A new entry for the key '$secret_key_name' has been successfully added in the vault file for targeted host group : " $host_group_name
		   else
			   echo "                                                                                     "
			   echo -e '\033[31m Sorry entered value and Confirm value does not matched for new secret key, Please try again ! \033[0m '
		   fi
                ;;
        2)
		echo "You have choosen: 2. Update value of the existing secret key." 
		echo
                echo "**Note: Value will be update only if the key is present in the file. "
                echo
                # value=$(update_key_value) #$host_group_name ;
                read -p 'Enter a secret key name for which you want to update the value: ' secret_key_name
		 
		 echo
		 read -s -p " New secret value : "  new_secret_value
		 echo
		 read -s -p " Confirm New secret value : "  confirm_new_secret_value

		 if [[ "$new_secret_value" == "$confirm_new_secret_value" ]]; then
			   sed -i "s/\($secret_key_name\).*\$/\1: \"$new_secret_value\"/"  $secret_storage_path$host_group_name$secret_storage_file_name
			   echo "                                                                                      "
			   echo " Success !!  Secrets has been updated successfully for targeted host group : " $host_group_name
	    	 else
			   echo "                                                                                     "
			   echo -e '\033[31m Sorry New secret value and Confirm secret value does not matched, Please try again ! \033[0m '
		 fi
		;;
        *)
                echo -e "\033[31m Sorry, I don't understand , Please try again ! \033[0m "
                ;;
    esac

   ansible-vault encrypt $secret_storage_path$host_group_name$secret_storage_file_name &>> utility_log.txt

else
   echo "                                                                                     "
   echo -e '\033[31m Oops! secrets not found for entered Host Group Name '$host_group_name' , Please try again ! \033[0m '
fi

echo "                                                                                      "
echo " ____________________________________________________________________________________ "
echo "                                                                                      "


#Function to update values for existing keys

update_key_value()
   {

        read -p 'Enter a secret key name for which you want to update the value: ' secret_key_name

           echo
           read -s -p " New secret value : "  new_secret_value
           echo
           read -s -p " Confirm New secret value : "  confirm_new_secret_value

           if [[ "$new_secret_value" == "$confirm_new_secret_value" ]]; then
                   sed -i "s/\($secret_key_name\).\$/\1: \"$new_secret_value\"/"  $secret_storage_path$host_group_name$secret_storage_file_name
                   echo "                                                                                      "
                   echo " Success !!  Secrets has been updated successfully for targeted host group : " $1
           else
                   echo "                                                                                     "
                   echo -e '\033[31m Sorry New secret value and Confirm secret value does not matched, Please try again ! \033[0m '
           fi

   }


#Function to add new key value pair
add_key_value()
   {
    echo "Any newly added key will be appended at the end of the file"
    echo
        read -p 'Enter new secret key: ' secret_key_name
        echo
        read -s -p 'Enter value for above secret key: ' secret_key_value
        echo
        read -s -p "Please confirm key value : "  confirm_secret_key_value

           if [[ "$secret_key_value" == "$confirm_secret_key_value" ]]; then
                   echo $secret_key_value": \""$confirm_secret_key_value "\"" >>  $secret_storage_path$host_group_name$secret_storage_file_name

                   echo "                                                                                      "
                   echo " Success !!  Secrets has been updated successfully for targeted host group : " $1
           else
                   echo "                                                                                     "
                   echo -e '\033[31m Sorry entered value and Confirm value does not matched for new secret key, Please try again ! \033[0m '
           fi

   }
