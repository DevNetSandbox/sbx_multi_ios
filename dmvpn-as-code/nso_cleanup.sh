echo "Shutting down virl simulation"
echo "=========================="
cd virl/sandbox
virl down nso
cd ../..

# launch NSO
make nso-clean
