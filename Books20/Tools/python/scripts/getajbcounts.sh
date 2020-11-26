for ajb in `ls ajb??_books.xml`; do
    entries=$(ppxml $ajb | grep "<Entry>" | wc | awk '{print $1}')
    references=$(ppxml $ajb | grep "<ReferenceOf>" | wc | awk '{print $1}')
    books=$(echo "$entries-$references" | bc | awk '{print $1}')
    echo $ajb "$entries" $references $books
done

      
